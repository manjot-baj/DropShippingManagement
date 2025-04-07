from django.contrib import messages
from django.shortcuts import redirect
from store.models import Store


class StoreRequiredMixin:
    """Base Mixin for store-based access control in CBVs."""

    required_role = None  # To be set in subclasses

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("login")  # Redirect if not authenticated
        try:
            if not Store.objects.filter(owner__user=request.user).exists():
                messages.error(request, "Store Required.")
                return redirect("store_view")  # Redirect if no store
        except:
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)
