from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import UserProfile


def get_profile(user):
    if not user.is_authenticated:
        return None
    return getattr(user, "profile", None)


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            profile = get_profile(request.user)
            if not profile or profile.role != role:
                return redirect("home")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
