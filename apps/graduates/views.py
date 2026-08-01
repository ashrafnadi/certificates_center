from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.administration.models import (
    users_profile,
    faculty,
    upload_error,
    transaction,
    history,
)
from apps.graduates.models import graduate, certificate


@login_required
def index(request):
    """
    Dashboard view showing role-based KPIs and statistics.
    Employees see data filtered by their selected faculty.
    Directors & Supervisors see full system overview.
    Auditors see verification-focused metrics.
    """
    user = request.user
    role = getattr(user, "role", "employee")
    is_admin = getattr(user, "isadmin", None) in ("1", "yes", "true", "True", "Yes")
    is_superuser = getattr(user, "is_superuser", False) or getattr(
        user, "is_staff", False
    )

    if request.user.is_superuser:
        request.user.is_admin = True
    elif hasattr(request.user, "profile"):
        if request.user.profile.role == "director":
            request.user.is_director = True
        elif request.user.profile.role == "supervisor":
            request.user.is_supervisor = True
        elif request.user.profile.role == "auditor":
            request.user.is_auditor = True
        elif request.user.profile.role == "employee":
            request.user.is_employee = True
        else:
            request.user.is_student = False
    else:
        request.user.is_student = False

    selected_faculty_id = request.session.get("selected_faculty_id")
    selected_faculty_name = request.session.get("selected_faculty_name", "")

    # Determine data scope
    if role == "employee" and selected_faculty_id:
        grad_filter = {"faculty_id": selected_faculty_id}
        scope_label = selected_faculty_name or "الكلية المختارة"
    else:
        grad_filter = {}
        scope_label = "جميع الكليات"

    # Graduate IDs for certificate filtering (schema uses plain IDs, not FKs)
    if grad_filter:
        graduate_ids = list(
            graduate.objects.filter(**grad_filter).values_list("graduate_id", flat=True)
        )
        cert_qs = certificate.objects.filter(graduate_id__in=graduate_ids)
    else:
        cert_qs = certificate.objects.all()

    # Core counts
    total_graduates = graduate.objects.filter(**grad_filter).count()
    total_certificates = cert_qs.count()
    printed_certificates = cert_qs.exclude(print_date=None).count()
    delivered_certificates = cert_qs.filter(delivered="1").count()
    pending_certificates = cert_qs.filter(print_date=None).count()

    # Percentages
    print_pct = (
        round((printed_certificates / total_certificates * 100), 1)
        if total_certificates
        else 0
    )
    pending_pct = (
        round((pending_certificates / total_certificates * 100), 1)
        if total_certificates
        else 0
    )
    deliver_pct = (
        round((delivered_certificates / total_certificates * 100), 1)
        if total_certificates
        else 0
    )

    # Build context
    context = {
        "user_role": role,
        "user_role_display": dict(users_profile.ROLE_CHOICES).get(role, role),
        "scope_label": scope_label,
        "selected_faculty_name": selected_faculty_name,
        # Core KPIs
        "total_graduates": total_graduates,
        "total_certificates": total_certificates,
        "printed_certificates": printed_certificates,
        "delivered_certificates": delivered_certificates,
        "pending_certificates": pending_certificates,
        "print_pct": print_pct,
        "pending_pct": pending_pct,
        "deliver_pct": deliver_pct,
        # Recent lists
        "recent_graduates": graduate.objects.filter(**grad_filter).order_by(
            "-graduate_id"
        )[:6],
        "recent_certificates": cert_qs.order_by("-certificate_date")[:5],
    }

    # ═══════════════════════════════════════════════════
    # DIRECTOR / SUPERVISOR KPIs
    # ═══════════════════════════════════════════════════
    if role in ("director", "supervisor") or is_admin or is_superuser:
        context["total_faculties"] = faculty.objects.count()
        context["total_users"] = users_profile.objects.count()
        context["upload_errors"] = upload_error.objects.count()
        context["recent_transactions"] = transaction.objects.order_by(
            "-transaction_date"
        )[:5]

        # Faculty breakdown with percentages
        breakdown = []
        all_grad_count = graduate.objects.count() or 1  # avoid div by zero
        for f in faculty.objects.all().order_by("faculty_ar_name"):
            count = graduate.objects.filter(faculty_id=f.faculty_id).count()
            if count > 0:
                breakdown.append(
                    {
                        "name": f.faculty_ar_name,
                        "count": count,
                        "id": f.faculty_id,
                        "pct": round((count / all_grad_count) * 100, 1),
                    }
                )
        context["faculty_breakdown"] = sorted(
            breakdown, key=lambda x: x["count"], reverse=True
        )[:8]

    # ═══════════════════════════════════════════════════
    # AUDITOR KPIs
    # ═══════════════════════════════════════════════════
    if role == "auditor" or is_admin or is_superuser:
        context["unchecked_graduates"] = (
            graduate.objects.filter(**grad_filter).exclude(ischeked="1").count()
        )

        hist_filter = {}
        if role == "employee" and selected_faculty_id:
            hist_filter["faculty_id"] = selected_faculty_id
        context["recent_history"] = history.objects.filter(**hist_filter).order_by(
            "-history_date"
        )[:5]

    return render(request, "graduate/index.html", context)
