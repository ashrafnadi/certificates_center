from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from apps.administration.models import (
    Faculty,
    Section,
    Specialization,
    Transaction,
    Upload_Error,
    Users_Profile,
)
from apps.graduates.models import Certificate, Graduate, History


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
        context["unchecked_graduates_supervisor"] = base_grad_qs.filter(
            Q(ischeked="Y") & Q(ischeked2="N")
        ).count()

        hist_filter = {}
        if role == "employee" and selected_faculty_id:
            hist_filter["faculty_id"] = selected_faculty_id
        context["recent_history"] = History.objects.filter(**hist_filter).order_by(
            "-history_date"
        )[:5]

    return render(request, "graduates/index.html", context)


@login_required
def graduate_list(request):
    """
    Graduate list view with role-based filtering:
    - Director/Supervisor/Superuser: All faculties → sections → specializations → graduates
    - Auditor: Login faculty only, ischeked='N', must select section → specialization
    - Employee: Login faculty only, must select section → specialization
    """
    user = request.user
    role = request.session.get("user_role") or getattr(user, "role", "employee")
    is_admin = request.session.get("user_is_admin", False)
    is_superuser = getattr(user, "is_staff", False)

    selected_faculty_id = request.session.get("selected_faculty_id")
    selected_faculty_name = request.session.get("selected_faculty_name", "")

    # ── Determine scope ──
    is_director = role in ("director", "supervisor") or is_admin or is_superuser

    # Faculties list (only for directors/supervisors/superusers)
    faculties = Faculty.objects.all().order_by("faculty_ar_name") if is_director else []

    # GET parameters
    faculty_id = request.GET.get("faculty_id")
    section_id = request.GET.get("section_id")
    specialization_id = request.GET.get("specialization_id")
    graduate_id = request.GET.get("graduate_id")

    # ── Faculty filter ──
    if is_director and faculty_id:
        current_faculty = get_object_or_404(Faculty, pk=faculty_id)
    elif not is_director and selected_faculty_id:
        current_faculty = get_object_or_404(Faculty, pk=selected_faculty_id)
        faculty_id = selected_faculty_id
    else:
        current_faculty = None

    # ── Sections list ──
    sections = []
    if current_faculty:
        sections = Section.objects.filter(faculty=current_faculty).order_by(
            "section_ar_namr"
        )

    # ── Specializations list ──
    specializations = []
    if section_id:
        specializations = Specialization.objects.filter(section_id=section_id).order_by(
            "specialization_ar_name"
        )

    # ── Graduates queryset ──
    graduates = Graduate.objects.none()
    if current_faculty and specialization_id:
        graduates = Graduate.objects.filter(
            faculty=current_faculty,
            specialization_id=specialization_id,
        )

        # Auditor: only unchecked graduates
        if role == "auditor":
            graduates = graduates.filter(ischeked="N")

        graduates = graduates.select_related(
            "nationality", "faculty", "specialization"
        ).order_by("-graduate_id")

    # ── Graduate detail ──
    selected_graduate = None
    certificates = []
    if graduate_id:
        selected_graduate = get_object_or_404(
            Graduate.objects.select_related(
                "nationality", "faculty", "specialization", "faculty_turn", "regulation"
            ),
            graduate_id=graduate_id,
        )
        certificates = Certificate.objects.filter(graduate_id=graduate_id).order_by(
            "-certificate_date"
        )

    context = {
        "user_role": role,
        "is_director": is_director,
        "faculties": faculties,
        "sections": sections,
        "specializations": specializations,
        "graduates": graduates,
        "selected_faculty": current_faculty,
        "selected_faculty_name": selected_faculty_name,
        "selected_section_id": section_id,
        "selected_specialization_id": specialization_id,
        "selected_graduate": selected_graduate,
        "certificates": certificates,
    }

    # HTMX partial rendering
    if request.headers.get("HX-Request"):
        if "section_id" in request.GET and "specialization_id" not in request.GET:
            return render(request, "graduates/partials/specializations.html", context)
        elif "specialization_id" in request.GET and "graduate_id" not in request.GET:
            return render(request, "graduates/partials/graduates_table.html", context)
        elif "graduate_id" in request.GET:
            return render(request, "graduates/partials/graduate_detail.html", context)

    return render(request, "graduates/graduate_list.html", context)
