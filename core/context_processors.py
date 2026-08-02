from django.conf import settings


def application_info(request):
    return {
        "APPLICATION_NAME": getattr(settings, "APPLICATION_NAME", "نظام بداية"),
        "APPLICATION_SLUG": getattr(settings, "APPLICATION_SLUG", "بداية"),
        "COPYRIGHT_NAME": getattr(settings, "COPYRIGHT_NAME", ""),
        "COPYRIGHT_YEAR": getattr(settings, "COPYRIGHT_YEAR", "2026"),
    }


def global_context(request):
    return {
        "APPLICATION_NAME": getattr(settings, "APPLICATION_NAME", "Certificate Center"),
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
        "DEBUG": settings.DEBUG,
        "user_role": request.session.get("user_role", ""),
        "user_is_admin": request.session.get("user_is_admin", False),
    }
