from django.conf import settings

from .decorators import get_profile


def google_maps(request):
    key = getattr(settings, "GOOGLE_MAPS_API_KEY", "")
    return {
        "GOOGLE_MAPS_API_KEY": key,
        "GOOGLE_MAPS_ENABLED": bool(key),
    }


def site_header(request):
    profile = get_profile(request.user) if request.user.is_authenticated else None
    return {
        "cp_user_profile": profile,
        "cp_user_role": profile.role if profile else "",
    }
