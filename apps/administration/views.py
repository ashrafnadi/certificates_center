import logging

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import LoginForm

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def user_login(request):
    """صفحة تسجيل الدخول مع التحقق من الدور والكلية"""
    if request.user.is_authenticated:
        return redirect("graduates:index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            selected_faculty = form.cleaned_data["faculty"]

            # ⬅️ Django يجرب كل الـ AUTHENTICATION_BACKENDS تلقائياً
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # التحقق من الدور والصلاحيات
                role = getattr(user, "role", None)
                is_admin = getattr(user, "isadmin", None)
                is_superuser = getattr(user, "is_superuser", False) or getattr(
                    user, "is_staff", False
                )

                # لو المستخدم من django.contrib.auth (superuser) ومش عنده profile
                # نعتبره مشرف/مدير وما نطلبش منه كلية
                if role is None and is_superuser:
                    role = "supervisor"  # أو 'director' حسب رغبتك
                    is_admin = "1"

                # المدقق والموظف ملزمين باختيار الكلية (ما عدا الـ admin / superuser)
                faculty_required = False
                if (
                    role in ("auditor", "employee")
                    and not is_admin
                    and not is_superuser
                ):
                    faculty_required = True

                if faculty_required and not selected_faculty:
                    form.add_error("faculty", "يجب اختيار الكلية للمدققين والموظفين")
                else:
                    login(request, user)

                    # حفظ الكلية المختارة في الجلسة
                    if selected_faculty:
                        request.session["selected_faculty_id"] = (
                            selected_faculty.faculty_id
                        )
                        request.session["selected_faculty_name"] = (
                            selected_faculty.faculty_ar_name
                        )
                    else:
                        request.session.pop("selected_faculty_id", None)
                        request.session.pop("selected_faculty_name", None)

                    # إعادة توجيه HTMX أو عادي
                    if request.headers.get("HX-Request"):
                        response = HttpResponse()
                        response["HX-Redirect"] = "/"
                        return response
                    return redirect("graduates:index")
            else:
                form.add_error(None, "اسم المستخدم أو كلمة المرور غير صحيحة")
                logger.warning(f"محاولة دخول فاشلة: {username}")
    else:
        form = LoginForm()

    context = {"form": form}

    if request.headers.get("HX-Request"):
        return render(request, "administration/partials/login_form.html", context)

    return render(request, "administration/login.html", context)


@require_http_methods(["GET", "POST"])
def user_logout(request):
    """تسجيل الخروج"""
    logout(request)
    return redirect("administration:login")
