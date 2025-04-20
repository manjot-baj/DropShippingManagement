from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from catalog.models import Company


class CompanyRequiredMixin:
    """Base Mixin for company-based access control in CBVs."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("login")

        try:
            has_company = Company.objects.filter(
                owner__user=request.user, is_deleted=False
            ).exists()
            if not has_company:
                return redirect("company_list")
        except Exception:
            logout(request)
            messages.error(
                request,
                "An error occurred while checking company access. You have been logged out.",
            )
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)
