import logging

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import LoginForm
from .models import Authenticated_User, Faculty, Users_Profile

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def user_login(request):
    """
    صفحة تسجيل الدخول مع التحقق من الدور والكلية

    - يتحقق من بيانات المستخدم عبر UsersProfileAuthBackend
    - للمدققين والموظفين: يتحقق من تسجيلهم في Authenticated_User
    - يعرض فقط الكليات المصرح بها في Authenticated_User
    - يخزن صلاحيات Authenticated_User في الجلسة
    """
    if request.user.is_authenticated:
        return redirect("graduates:index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            selected_faculty = form.cleaned_data["faculty"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # ── Look up the actual Users_Profile by username ──
                # This avoids relying on user being a Users_Profile instance
                try:
                    users_profile = Users_Profile.objects.get(user_name=username)
                except Users_Profile.DoesNotExist:
                    form.add_error(None, "لم يتم العثور على ملف المستخدم")
                    context = {"form": form}
                    return render(request, "administration/login.html", context)

                # ── Determine role & admin status ──
                role = users_profile.role
                is_admin = users_profile.isadmin in (
                    "1",
                    "yes",
                    "true",
                    "True",
                    "Yes",
                )
                is_staff = getattr(user, "is_staff", False)

                # Django superuser without profile → treat as director
                if role is None and is_staff:
                    role = "director"
                    is_admin = True

                # Fallback if role still None
                if role is None:
                    role = "employee"

                # ── Authenticated_User faculty assignments ──
                # FIX: Pass the actual Users_Profile instance, not the auth user
                user_assignments = Authenticated_User.objects.filter(
                    authorize_user_id=users_profile
                ).select_related("faculty_id")

                assigned_faculty_ids = [
                    a.faculty_id_id for a in user_assignments if a.faculty_id_id
                ]
                has_assignments = bool(assigned_faculty_ids)

                # Build restricted faculties queryset
                allowed_faculties = None
                if assigned_faculty_ids:
                    allowed_faculties = Faculty.objects.filter(
                        faculty_id__in=assigned_faculty_ids
                    ).order_by("faculty_ar_name")

                # ── Faculty requirement ──
                faculty_required = (
                    role in ("auditor", "employee") and not is_admin and not is_staff
                )

                if faculty_required:
                    if not has_assignments:
                        form.add_error(
                            None,
                            "لم يتم تعيين كلية لهذا المستخدم. يرجى التواصل مع المسؤول.",
                        )
                    elif not selected_faculty:
                        form.add_error("faculty", "يجب اختيار الكلية")
                        if allowed_faculties is not None:
                            form.fields["faculty"].queryset = allowed_faculties
                    elif selected_faculty.faculty_id not in assigned_faculty_ids:
                        form.add_error(
                            "faculty",
                            "غير مصرح بالوصول إلى هذه الكلية. يرجى اختيار كلية مسموح بها.",
                        )
                        if allowed_faculties is not None:
                            form.fields["faculty"].queryset = allowed_faculties
                    else:
                        # Valid faculty selected — get auth record
                        auth_record = user_assignments.get(faculty_id=selected_faculty)
                        _do_login(
                            request,
                            user,
                            users_profile,
                            role,
                            is_admin,
                            selected_faculty,
                            auth_record,
                        )
                        return _htmx_or_redirect(request)
                else:
                    # Director / Supervisor / Admin — faculty optional
                    auth_record = None
                    if (
                        selected_faculty
                        and has_assignments
                        and selected_faculty.faculty_id in assigned_faculty_ids
                    ):
                        auth_record = user_assignments.get(faculty_id=selected_faculty)

                    _do_login(
                        request,
                        user,
                        users_profile,
                        role,
                        is_admin,
                        selected_faculty,
                        auth_record,
                    )
                    return _htmx_or_redirect(request)
            else:
                form.add_error(None, "اسم المستخدم أو كلمة المرور غير صحيحة")
                logger.warning(f"محاولة دخول فاشلة: {username}")
    else:
        form = LoginForm()

    context = {"form": form}

    if request.headers.get("HX-Request"):
        return render(request, "administration/partials/login_form.html", context)

    return render(request, "administration/login.html", context)


def _do_login(
    request, auth_user, users_profile, role, is_admin, selected_faculty, auth_record
):
    """
    تنفيذ تسجيل الدخول وتخزين بيانات الجلسة

    auth_user: the user object returned by authenticate() (for Django login)
    users_profile: the actual Users_Profile instance (for our custom queries)
    """
    login(request, auth_user)

    # Role & admin status
    request.session["user_role"] = role
    request.session["user_is_admin"] = is_admin

    # Store Users_Profile ID for reference
    request.session["users_profile_id"] = users_profile.id

    # Selected faculty
    if selected_faculty:
        request.session["selected_faculty_id"] = selected_faculty.faculty_id
        request.session["selected_faculty_name"] = selected_faculty.faculty_ar_name
    else:
        request.session.pop("selected_faculty_id", None)
        request.session.pop("selected_faculty_name", None)

    # Authenticated_User permissions
    if auth_record:
        request.session["auth_user_id"] = auth_record.authunticated_user_id
        request.session["perm_isadd"] = auth_record.isadd
        request.session["perm_isedit"] = auth_record.isedit
        request.session["perm_isdelete"] = auth_record.isdelete
        request.session["perm_isprint"] = auth_record.isprint
        request.session["perm_iscommit"] = auth_record.iscommit
        request.session["perm_isview"] = auth_record.isview
    else:
        # Director/Admin without auth record → full permissions
        request.session["auth_user_id"] = None
        request.session["perm_isadd"] = True
        request.session["perm_isedit"] = True
        request.session["perm_isdelete"] = True
        request.session["perm_isprint"] = True
        request.session["perm_iscommit"] = True
        request.session["perm_isview"] = True


def _htmx_or_redirect(request):
    """إرجاع إعادة توجيه HTMX أو عادية."""
    if request.headers.get("HX-Request"):
        response = HttpResponse()
        response["HX-Redirect"] = "/"
        return response
    return redirect("graduates:index")


@require_http_methods(["GET", "POST"])
def user_logout(request):
    """تسجيل الخروج مع مسح بيانات الجلسة."""
    logout(request)
    return redirect("administration:login")
