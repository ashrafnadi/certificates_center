import logging
import traceback

from django.conf import settings
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

logger = logging.getLogger(__name__)


@login_required
def index(request):
    """Dashboard view showing role-based KPIs and statistics."""
    user = request.user
    role = request.session.get("user_role") or getattr(user, "role", "employee")
    is_admin = request.session.get("user_is_admin", False)
    is_superuser = getattr(user, "is_staff", False)

    if is_superuser and not hasattr(user, "is_admin"):
        user.is_admin = True

    selected_faculty_id = request.session.get("selected_faculty_id")
    selected_faculty_name = request.session.get("selected_faculty_name", "")

    if role == "employee" and selected_faculty_id:
        grad_filter = {"faculty_id": selected_faculty_id}
        scope_label = selected_faculty_name or "الكلية المختارة"
    else:
        grad_filter = {}
        scope_label = "جميع الكليات"

    base_grad_qs = Graduate.objects.filter(**grad_filter)

    if grad_filter:
        cert_qs = Certificate.objects.filter(graduate__in=base_grad_qs)
    else:
        cert_qs = Certificate.objects.all()

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
        # FIX: Added select_related for regulation__degree and specialization
        "recent_graduates": base_grad_qs.select_related(
            "faculty", "specialization", "regulation", "regulation__degree"
        ).order_by("-graduate_id")[:8],
        "recent_certificates": cert_qs.order_by("-certificate_date")[:8],
    }

    if role in ("director", "supervisor") or is_admin or is_superuser:
        context["total_faculties"] = Faculty.objects.count()
        context["total_users"] = Users_Profile.objects.count()
        context["upload_errors"] = Upload_Error.objects.count()

        context["recent_transactions"] = (
            Transaction.objects.annotate(graduate_count=Count("graduate"))
            .filter(graduate_count__gt=0)
            .select_related("faculty")
            .order_by("-transaction_date")[:8]
        )

        all_grad_count = Graduate.objects.count() or 1

        breakdown_qs = (
            Faculty.objects.annotate(
                grad_count=Count(
                    "graduates",
                    filter=Q(graduates__ischeked="Y") | Q(graduates__ischeked2="Y"),
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
    Graduate list view with role-based filtering + global search.
    """
    user = request.user
    role = request.session.get("user_role") or getattr(user, "role", "employee")
    is_admin = request.session.get("user_is_admin", False)
    is_superuser = getattr(user, "is_staff", False)

    selected_faculty_id = request.session.get("selected_faculty_id")
    selected_faculty_name = request.session.get("selected_faculty_name", "")

    is_director = role in ("director", "supervisor") or is_admin or is_superuser

    faculties = Faculty.objects.all().order_by("faculty_ar_name") if is_director else []

    # GET parameters
    faculty_id = request.GET.get("faculty_id")
    section_id = request.GET.get("section_id")
    specialization_id = request.GET.get("specialization_id")
    graduate_id = request.GET.get("graduate_id")
    search_query = request.GET.get("q", "").strip()

    # ── Faculty resolution ──
    current_faculty = None
    resolved_faculty_id = None

    if is_director and faculty_id:
        try:
            current_faculty = Faculty.objects.get(pk=int(faculty_id))
            resolved_faculty_id = faculty_id
        except (Faculty.DoesNotExist, ValueError, TypeError):
            current_faculty = None
            resolved_faculty_id = None
    elif not is_director and selected_faculty_id:
        try:
            current_faculty = Faculty.objects.get(pk=int(selected_faculty_id))
            resolved_faculty_id = str(selected_faculty_id)
        except (Faculty.DoesNotExist, ValueError, TypeError):
            current_faculty = None
            resolved_faculty_id = None

    # ── Sections list ──
    sections = []
    if current_faculty:
        sections = Section.objects.filter(faculty=current_faculty).order_by(
            "section_ar_name"
        )

    # ── Specializations list ──
    specializations = []
    if section_id:
        try:
            specializations = Specialization.objects.filter(
                section_id=int(section_id)
            ).order_by("specialization_ar_name")
        except (ValueError, TypeError):
            specializations = []

    # ── Graduates queryset ──
    graduates = Graduate.objects.none()
    debug_info = {}
    error_message = None

    # SEARCH MODE
    if search_query:
        try:
            search_filter = (
                Q(graduate_ar_name__icontains=search_query)
                | Q(graduate_en_name__icontains=search_query)
                | Q(graduate_id_card__icontains=search_query)
                | Q(graduate_ar_pob__icontains=search_query)
                | Q(graduate_en_pob__icontains=search_query)
                | Q(grade_name_ar__icontains=search_query)
                | Q(grade_name_en__icontains=search_query)
                | Q(grade_letter__icontains=search_query)
                | Q(ic_card_init__icontains=search_query)
                | Q(graduate_notes__icontains=search_query)
                | Q(nationality__nationality_ar_name__icontains=search_query)
                | Q(nationality__nationality_en_name__icontains=search_query)
                | Q(faculty__faculty_ar_name__icontains=search_query)
                | Q(faculty__faculty_en_name__icontains=search_query)
                | Q(specialization__specialization_ar_name__icontains=search_query)
                | Q(specialization__specialization_en_name__icontains=search_query)
                | Q(faculty_turn__turn_ar_name__icontains=search_query)
                | Q(faculty_turn__turn_en_name__icontains=search_query)
                | Q(regulation__regulation_ar_name__icontains=search_query)
            )

            if not is_director and selected_faculty_id:
                graduates = Graduate.objects.filter(
                    faculty_id=int(selected_faculty_id)
                ).filter(search_filter)
            else:
                graduates = Graduate.objects.filter(search_filter)

            graduates = graduates.select_related(
                "nationality", "faculty", "specialization"
            ).order_by("-graduate_id")

            debug_info = {
                "mode": "search",
                "query": search_query,
                "count": graduates.count(),
            }
        except Exception as e:
            error_message = f"Search error: {str(e)}"
            logger.exception("Search query failed")

    # CASCADE MODE
    elif current_faculty and specialization_id:
        try:
            spec_id = int(specialization_id)
            fac_id = current_faculty.faculty_id

            graduates = Graduate.objects.filter(
                faculty_id=fac_id,
                specialization_id=spec_id,
            )
            if role == "auditor":
                graduates = graduates.filter(ischeked="N")

            graduates = graduates.select_related(
                "nationality", "faculty", "specialization"
            ).order_by("-graduate_id")

            debug_info = {
                "mode": "cascade",
                "faculty_id": fac_id,
                "specialization_id": spec_id,
                "count": graduates.count(),
            }
        except Exception as e:
            error_message = f"Cascade error: {str(e)}"
            logger.exception("Cascade query failed")
            debug_info = {
                "mode": "cascade_error",
                "error": str(e),
                "traceback": traceback.format_exc(),
            }

    # ── Graduate detail ──
    selected_graduate = None
    certificates = []
    if graduate_id:
        try:
            # FIX: Added regulation__degree to select_related
            selected_graduate = get_object_or_404(
                Graduate.objects.select_related(
                    "nationality",
                    "faculty",
                    "specialization",
                    "faculty_turn",
                    "regulation",
                    "regulation__degree",
                ),
                graduate_id=int(graduate_id),
            )
            certificates = selected_graduate.certificate_set.all().order_by(
                "-certificate_date"
            )
        except (ValueError, TypeError):
            selected_graduate = None

    context = {
        "user_role": role,
        "is_director": is_director,
        "faculties": faculties,
        "sections": sections,
        "specializations": specializations,
        "graduates": graduates,
        "selected_faculty": current_faculty,
        "selected_faculty_id": resolved_faculty_id,
        "selected_faculty_name": selected_faculty_name,
        "selected_section_id": section_id or "",
        "selected_specialization_id": specialization_id or "",
        "selected_graduate": selected_graduate,
        "certificates": certificates,
        "search_query": search_query,
        "debug_info": debug_info if settings.DEBUG else None,
        "error_message": error_message if settings.DEBUG else None,
    }

    # HTMX partial rendering
    is_htmx = request.headers.get("HX-Request") == "true"
    if is_htmx:
        has_grad = bool(graduate_id)
        has_search = bool(search_query)
        has_spec = bool(specialization_id)
        has_section = bool(section_id)
        has_faculty = bool(faculty_id)

        if has_grad:
            return render(
                request, "graduates/partials/graduate_detail_modal.html", context
            )
        if has_search:
            return render(request, "graduates/partials/graduates_table.html", context)
        if has_spec:
            return render(request, "graduates/partials/graduates_table.html", context)
        if has_section:
            return render(request, "graduates/partials/specializations.html", context)
        if has_faculty:
            return render(request, "graduates/partials/faculty_changed.html", context)

    return render(request, "graduates/graduate_list.html", context)
