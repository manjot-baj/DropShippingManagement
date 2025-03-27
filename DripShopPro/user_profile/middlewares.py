from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.shortcuts import redirect


def role_required(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == required_role:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Unauthorized access.")
                return redirect("login")

        return _wrapped_view

    return decorator
