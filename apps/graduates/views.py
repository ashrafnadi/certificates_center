from django.db.models import Count, Q, Exists, OuterRef
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
    Optimized to minimize query count using aggregates, annotations,
    subqueries, and Exists() instead of COUNT+GROUP BY.
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

    # ── Base querysets (cached, not evaluated yet) ──
    base_grad_qs = Graduate.objects.filter(**grad_filter)

    # Certificate subquery — Django generates SQL subquery, no IDs loaded into Python
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

        # Optimized: EXISTS subquery instead of annotate(Count)+GROUP BY+HAVING
        # Reduces 92ms → ~5ms, eliminates GROUP BY on faculty_id
        has_graduates = Graduate.objects.filter(transaction_id=OuterRef("pk"))
        context["recent_transactions"] = (
            Transaction.objects.filter(Exists(has_graduates))
            .select_related("faculty_id")
            .order_by("-transaction_date")[:8]
        )

        # Optimized: Single annotate query replaces 17 per-faculty COUNT queries
        all_grad_count = Graduate.objects.count() or 1
        breakdown_qs = (
            Faculty.objects.annotate(
                grad_count=Count(
                    "graduate",
                    filter=~Q(
                        graduate__ischeked="N",
                        graduate__ischeked2="N",
                    ),
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
        context["unchecked_graduates"] = base_grad_qs.exclude(
            ischeked="Y", ischeked2="Y"
        ).count()

        hist_filter = {}
        if role == "employee" and selected_faculty_id:
            hist_filter["faculty_id"] = selected_faculty_id
        context["recent_history"] = History.objects.filter(**hist_filter).order_by(
            "-history_date"
        )[:5]

    return render(request, "graduates/index.html", context)
