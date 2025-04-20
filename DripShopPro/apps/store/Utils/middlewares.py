from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from store.models import Store


class StoreRequiredMixin:
    """Base Mixin for store-based access control in CBVs."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("login")

        try:
            has_store = Store.objects.filter(owner__user=request.user).exists()
            if not has_store:
                return redirect("store_view")
        except Exception:
            logout(request)
            messages.error(
                request,
                "An error occurred while checking store access. You have been logged out.",
            )
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)
