from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.core.cache import cache

from .models import Users_Profile


class UsersProfileAuthBackend(BaseBackend):
    """
    يتحقق من اسم المستخدم وكلمة المرور مقابل جدول users_profile
    يدعم كلمات المرور المشفرة (Django hashes) والنصوص العادية (legacy)
    """

    CACHE_TIMEOUT = 300  # 5 minutes

    def _build_user(self, profile):
        """Build a Django-compatible user object from a Users_Profile instance."""
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

        # Use regular functions instead of lambdas for picklability / caching compatibility
        def _get_session_auth_hash(p=profile):
            return str(p.user_id)

        def _get_username(p=profile):
            return p.user_name

        profile.get_session_auth_hash = _get_session_auth_hash
        profile.get_username = _get_username
        return profile

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

        # Invalidate cache on successful auth (in case profile was updated)
        cache.delete(f"auth_backend:user:{profile.user_id}")
        return self._build_user(profile)

    def get_user(self, user_id):
        """Fetch user with simple caching to avoid redundant DB hits."""
        cache_key = f"auth_backend:user:{user_id}"

        # Check cache first (stores a lightweight marker, not the full object)
        cached_id = cache.get(cache_key)
        if cached_id is not None:
            try:
                profile = Users_Profile.objects.get(pk=user_id)
                return self._build_user(profile)
            except Users_Profile.DoesNotExist:
                cache.delete(cache_key)
                return None

        try:
            profile = Users_Profile.objects.get(pk=user_id)
            user = self._build_user(profile)
            cache.set(cache_key, profile.user_id, timeout=self.CACHE_TIMEOUT)
            return user
        except Users_Profile.DoesNotExist:
            return None
