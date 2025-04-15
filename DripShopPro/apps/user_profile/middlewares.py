from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from user_profile.models import UserProfile


class RoleRequiredMixin:
    """Base Mixin for role-based access control in CBVs."""

    required_role = None  # To be set in subclasses

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("login")

        try:
            user_profile = request.user.userprofile
            user_role = getattr(user_profile, "role", None)

            if user_role != self.required_role:
                logout(request)
                messages.error(
                    request, "Unauthorized access. You have been logged out."
                )
                return redirect("login")

            if user_role in ["Merchant", "Vendor"]:
                is_approved = getattr(user_profile, "is_approved", None)
                if not is_approved:
                    logout(request)
                    messages.error(
                        request,
                        "Your account is pending admin approval. You have been logged out.",
                    )
                    return redirect("login")

        except UserProfile.DoesNotExist:
            logout(request)
            messages.error(request, "User profile not found. You have been logged out.")
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)
