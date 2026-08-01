from django.conf import settings


def application_info(request):
    return {
        "APPLICATION_NAME": getattr(settings, "APPLICATION_NAME", "نظام بداية"),
        "APPLICATION_SLUG": getattr(settings, "APPLICATION_SLUG", "بداية"),
        "COPYRIGHT_NAME": getattr(settings, "COPYRIGHT_NAME", ""),
        "COPYRIGHT_YEAR": getattr(settings, "COPYRIGHT_YEAR", "2026"),
    }
