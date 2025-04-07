import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from user_profile.middlewares import RoleRequiredMixin
from store.models import Store
from store.Forms.store_forms import StoreForm
from user_profile.models import UserProfile

logger = logging.getLogger("error_log")


class StoreView(RoleRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        try:
            store = (
                Store.objects.select_related("owner")
                .filter(
                    owner__user=request.user,
                    is_deleted=False,
                )
                .first()
            )

            return render(request, "merchant/store/store_view.html", {"store": store})
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching store.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching store."},
                status=500,
            )


class StoreCreateView(RoleRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        form = StoreForm(user=request.user)
        return render(request, "merchant/store/store_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        try:
            form = StoreForm(request.POST, request.FILES, user=request.user)

            if form.is_valid():
                with transaction.atomic():
                    store = form.save(commit=False)
                    store.owner = get_object_or_404(
                        UserProfile,
                        user=request.user,
                        role="Merchant",
                    )
                    store.save()
                messages.success(request, "Store created successfully.")
                return redirect("store_view")

            messages.error(request, "Invalid store form.")
            return render(request, "merchant/store/store_form.html", {"form": form})
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error creating store.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error creating store."},
                status=500,
            )


class StoreUpdateView(RoleRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, pk, *args, **kwargs):
        try:
            store = get_object_or_404(
                Store,
                pk=pk,
                owner__user=request.user,
                is_deleted=False,
            )
            form = StoreForm(instance=store, user=request.user)
            return render(
                request,
                "merchant/store/store_form.html",
                {"form": form, "store": store},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching store for editing.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error loading store."},
                status=500,
            )

    def post(self, request, pk, *args, **kwargs):
        try:
            store = get_object_or_404(
                Store,
                pk=pk,
                owner__user=request.user,
                is_deleted=False,
            )
            form = StoreForm(
                request.POST, request.FILES, instance=store, user=request.user
            )

            if form.is_valid():
                with transaction.atomic():
                    store = form.save()
                messages.success(request, "Store updated successfully.")
                return redirect("store_view")

            messages.error(request, "Invalid store form.")
            return render(
                request,
                "merchant/store/store_form.html",
                {"form": form, "store": store},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error updating store.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error updating store."},
                status=500,
            )


class StoreDeleteView(RoleRequiredMixin, View):
    required_role = "Merchant"

    def post(self, request, pk, *args, **kwargs):
        try:
            store = get_object_or_404(
                Store,
                pk=pk,
                owner__user=request.user,
                is_deleted=False,
            )
            store.delete()
            messages.success(request, "Store deleted successfully.")
            return JsonResponse(
                {"success": True, "message": "Store deleted successfully."}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error deleting store.")
            return JsonResponse(
                {"success": False, "message": "Error deleting store."}, status=500
            )
