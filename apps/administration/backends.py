from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from .models import Users_Profile


class UsersProfileAuthBackend(BaseBackend):
    """
    يتحقق من اسم المستخدم وكلمة المرور مقابل جدول users_profile
    يدعم كلمات المرور المشفرة (Django hashes) والنصوص العادية (legacy)
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        try:
            profile = Users_Profile.objects.get(user_name=username)
        except Users_Profile.DoesNotExist:
            return None

        # التحقق من كلمة المرور
        password_valid = False
        if profile.user_password.startswith(
            ("pbkdf2_sha256$", "bcrypt", "argon2", "scrypt")
        ):
            password_valid = check_password(password, profile.user_password)
        else:
            password_valid = profile.user_password == password

        if not password_valid:
            return None

        # إضافة واجهة المستخدم المطلوبة لنظام Django auth
        profile.backend = "apps.administration.backends.UsersProfileAuthBackend"
        profile.is_authenticated = True
        profile.is_active = True
        profile.is_staff = profile.isadmin not in (
            None,
            "",
            "0",
            "no",
            "false",
            "No",
            "False",
        )
        profile.is_superuser = profile.is_staff
        profile.pk = profile.user_id
        profile.id = profile.user_id
        profile.username = profile.user_name
        profile.email = profile.user_email or ""
        profile.first_name = profile.user_short_name or ""
        profile.last_name = ""
        profile.get_session_auth_hash = lambda self=profile: str(self.user_id)
        profile.get_username = lambda self=profile: self.user_name

        return profile

    def get_user(self, user_id):
        try:
            profile = Users_Profile.objects.get(pk=user_id)
            profile.backend = "apps.administration.backends.UsersProfileAuthBackend"
            profile.is_authenticated = True
            profile.is_active = True
            profile.is_staff = profile.isadmin not in (
                None,
                "",
                "0",
                "no",
                "false",
                "No",
                "False",
            )
            profile.is_superuser = profile.is_staff
            profile.pk = profile.user_id
            profile.id = profile.user_id
            profile.username = profile.user_name
            profile.email = profile.user_email or ""
            profile.first_name = profile.user_short_name or ""
            profile.last_name = ""
            profile.get_session_auth_hash = lambda self=profile: str(self.user_id)
            profile.get_username = lambda self=profile: self.user_name
            return profile
        except Users_Profile.DoesNotExist:
            return None
