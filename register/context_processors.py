from django.conf import settings


def google_maps(request):
    key = getattr(settings, "GOOGLE_MAPS_API_KEY", "")
    return {
        "GOOGLE_MAPS_API_KEY": key,
        "GOOGLE_MAPS_ENABLED": bool(key),
    }
