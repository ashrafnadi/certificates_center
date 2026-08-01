from django.db.models import Count, Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.administration.models import (
    Users_Profile,
    Faculty,
    Upload_Error,
    Transaction,
)
from apps.graduates.models import Graduate, Certificate, History


@login_required
def index(request):
    """
    Dashboard view showing role-based KPIs and statistics.
    """
    user = request.user
    role = request.session.get("user_role") or getattr(user, "role", "employee")
    is_admin = request.session.get("user_is_admin", False)
    is_superuser = getattr(user, "is_staff", False)

    # ── Role flags ──
    if is_superuser:
        request.user.is_admin = True
    elif hasattr(request.user, "profile"):
        setattr(request.user, f"is_{request.user.profile.role}", True)

    selected_faculty_id = request.session.get("selected_faculty_id")
    selected_faculty_name = request.session.get("selected_faculty_name", "")

    # ── Data scope ──
    if role == "employee" and selected_faculty_id:
        grad_filter = {"faculty_id": selected_faculty_id}
        scope_label = selected_faculty_name or "الكلية المختارة"
    else:
        grad_filter = {}
        scope_label = "جميع الكليات"

    # ── Base querysets ──
    base_grad_qs = Graduate.objects.filter(**grad_filter)

    # Certificate subquery via SQL IN (SELECT ...)
    if grad_filter:
        cert_qs = Certificate.objects.filter(
            graduate_id__in=base_grad_qs.values("graduate_id")
        )
    else:
        cert_qs = Certificate.objects.all()

    # ── Core KPIs: ALL certificate stats in ONE aggregate query ──
    cert_stats = cert_qs.aggregate(
        total=Count("certificate_id"),
        printed=Count("certificate_id", filter=Q(print_date__isnull=False)),
        delivered=Count("certificate_id", filter=Q(delivered="1")),
        pending=Count("certificate_id", filter=Q(print_date__isnull=True)),
    )

    total_graduates = base_grad_qs.count()
    total_certificates = cert_stats["total"]
    printed_certificates = cert_stats["printed"]
    delivered_certificates = cert_stats["delivered"]
    pending_certificates = cert_stats["pending"]

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

    context = {
        "user_role": role,
        "user_role_display": (
            "مدير النظام"
            if is_superuser
            else dict(Users_Profile.ROLE_CHOICES).get(role, role)
        ),
        "scope_label": scope_label,
        "selected_faculty_name": selected_faculty_name,
        "total_graduates": total_graduates,
        "total_certificates": total_certificates,
        "printed_certificates": printed_certificates,
        "delivered_certificates": delivered_certificates,
        "pending_certificates": pending_certificates,
        "print_pct": print_pct,
        "pending_pct": pending_pct,
        "deliver_pct": deliver_pct,
        # Recent lists
        "recent_graduates": base_grad_qs.select_related("faculty").order_by(
            "-graduate_id"
        )[:8],
        "recent_certificates": cert_qs.order_by("-certificate_date")[:8],
    }

    # ═══════════════════════════════════════════════════════════════
    # DIRECTOR / SUPERVISOR KPIs
    # ═══════════════════════════════════════════════════════════════
    if role in ("director", "supervisor") or is_admin or is_superuser:
        context["total_faculties"] = Faculty.objects.count()
        context["total_users"] = Users_Profile.objects.count()
        context["upload_errors"] = Upload_Error.objects.count()

        # Fast EXISTS subquery
        context["recent_transactions"] = (
            Transaction.objects.annotate(graduate_count=Count("graduate"))
            .filter(graduate_count__gt=0)
            .select_related("faculty")
            .order_by("-transaction_date")[:8]
        )

        # ── Faculty breakdown ──
        if grad_filter:
            all_grad_count = Graduate.objects.count() or 1
        else:
            all_grad_count = total_graduates or 1

        breakdown_qs = (
            Faculty.objects.annotate(
                grad_count=Count(
                    "graduate",
                    filter=Q(graduate__ischeked="Y") | Q(graduate__ischeked2="Y"),
                )
            )
            .filter(grad_count__gt=0)
            .order_by("-grad_count")[:8]
        )

        context["faculty_breakdown"] = [
            {
                "name": f.faculty_ar_name,
                "count": f.grad_count,
                "id": f.faculty_id,
                "pct": round((f.grad_count / all_grad_count) * 100, 1),
            }
            for f in breakdown_qs
        ]

    # ═══════════════════════════════════════════════════════════════
    # AUDITOR KPIs
    # ═══════════════════════════════════════════════════════════════
    if role == "auditor" or is_admin or is_superuser:
        context["unchecked_graduates"] = base_grad_qs.filter(
            Q(ischeked="N") & Q(ischeked2="N")
        ).count()
        context["unchecked_graduates_supervisor"] = base_grad_qs.filter(Q(ischeked="Y") & Q(ischeked2="N")).count()

        hist_filter = {}
        if role == "employee" and selected_faculty_id:
            hist_filter["faculty_id"] = selected_faculty_id
        context["recent_history"] = History.objects.filter(**hist_filter).order_by(
            "-history_date"
        )[:5]

    return render(request, "graduates/index.html", context)
