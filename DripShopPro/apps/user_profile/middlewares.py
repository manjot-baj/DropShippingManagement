from django.contrib import messages
from django.shortcuts import redirect


class RoleRequiredMixin:
    """Base Mixin for role-based access control in CBVs."""

    required_role = None  # To be set in subclasses

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("login")  # Redirect if not authenticated

        user_role = getattr(request.user.userprofile, "role", None)
        if user_role != self.required_role:
            messages.error(request, "Unauthorized access.")
            return redirect("login")  # Redirect if role mismatch

        return super().dispatch(request, *args, **kwargs)
