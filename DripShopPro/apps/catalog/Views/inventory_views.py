import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from user_profile.middlewares import RoleRequiredMixin
from catalog.models import Inventory
from catalog.Forms.inventory_forms import InventoryForm
from django.contrib import messages

logger = logging.getLogger("error_log")  # Centralized logger


# List all Inventory (for vendor)
class InventoryListView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            inventorys = Inventory.objects.select_related("company", "product").filter(
                is_deleted=False,
            )
            return render(
                request,
                "vendor/inventory/inventory_list.html",
                {"inventorys": inventorys},
            )
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching categories."},
                status=500,
            )


# Create a new Inventory
class InventoryCreateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        form = InventoryForm(user=request.user)
        return render(request, "vendor/inventory/inventory_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        try:
            form = InventoryForm(request.POST, user=request.user)

            if form.is_valid():
                with transaction.atomic():
                    inventory = form.save(commit=False)
                    inventory.product.inside_inventory = True
                    inventory.product.save()
                    inventory.save()
                return redirect("inventory_list")
            return render(
                request, "vendor/inventory/inventory_form.html", {"form": form}
            )
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error creating inventory."},
                status=500,
            )


# Update an existing Inventory
class InventoryUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, pk, *args, **kwargs):
        inventory = get_object_or_404(
            Inventory,
            pk=pk,
            is_deleted=False,
        )
        form = InventoryForm(instance=inventory, user=request.user)
        return render(
            request,
            "vendor/inventory/inventory_form.html",
            {"form": form, "inventory": inventory},
        )

    def post(self, request, pk, *args, **kwargs):
        try:
            inventory = get_object_or_404(
                Inventory,
                pk=pk,
                is_deleted=False,
            )
            form = InventoryForm(request.POST, instance=inventory, user=request.user)

            if form.is_valid():
                with transaction.atomic():
                    inventory = form.save(commit=False)
                    inventory.product.inside_inventory = True
                    inventory.product.save()
                    inventory.save()
                return redirect("inventory_list")
            return render(
                request,
                "vendor/inventory/inventory_form.html",
                {"form": form, "inventory": inventory},
            )
        except Exception:
            logger.error(traceback.format_exc())
            return render(
                request,
                "vendor/error.html",
                {"message": "Error updating inventory."},
                status=500,
            )


# Delete a inventory
class InventoryDeleteView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, pk, *args, **kwargs):
        try:
            inventory = get_object_or_404(
                Inventory,
                pk=pk,
                is_deleted=False,
            )
            inventory.product.inside_inventory = False
            inventory.product.save()
            inventory.is_deleted = True
            inventory.save()
            return JsonResponse(
                {"success": True, "message": "Inventory deleted successfully."}
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {"success": False, "message": "Error deleting inventory."}, status=500
            )


# Add or Remove From Catalog
class InventoryBulkCatalogUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, *args, **kwargs):
        try:
            ids = request.POST.getlist("inventory_ids")
            action = request.POST.get("action")

            if not ids or action not in ["add", "remove"]:
                messages.error(request, "Invalid selection or action.")
                return redirect("inventory_list")

            inventories = Inventory.objects.filter(
                id__in=ids, is_deleted=False, company__owner__user=request.user
            )

            update_value = True if action == "add" else False
            inventories.update(catalog_display=update_value)

            messages.success(
                request,
                f"{inventories.count()} inventory item(s) updated: catalog display set to {update_value}.",
            )
            return redirect("inventory_list")
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error updating catalog display.")
            return redirect("inventory_list")
