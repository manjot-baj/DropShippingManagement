import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from user_profile.middlewares import RoleRequiredMixin
from catalog.models import Inventory, Company, Product, ProductImage
from catalog.Forms.inventory_forms import InventoryForm

logger = logging.getLogger("error_log")


class CompanyProductCatalogView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, company_id, *args, **kwargs):
        try:
            company = get_object_or_404(
                Company,
                pk=company_id,
                owner__user=request.user,
                is_deleted=False,
            )
            catalogs = []
            inventorys = Inventory.objects.select_related("company", "product").filter(
                is_deleted=False,
                company=company,
                catalog_display=True,
            )
            for inventory in inventorys:
                catalogs.append(
                    {
                        "product": inventory.product.name,
                        "description": inventory.product.description,
                        "category": inventory.product.category.name,
                        "price": inventory.price,
                        "stock": inventory.stock,
                        "product_imgs": ProductImage.objects.filter(
                            product=inventory.product, is_deleted=False
                        ),
                        "product_single_img": ProductImage.objects.filter(
                            product=inventory.product, is_deleted=False
                        ).first(),
                        "company": inventory.company.name,
                        "company_id": inventory.company.pk,
                        "product_id": inventory.product.pk,
                        "inventory_id": inventory.pk,
                    }
                )
            return render(
                request,
                "vendor/catalog/catalog.html",
                {"catalogs": catalogs},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching catalog data.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching catalogs."},
                status=500,
            )


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
            messages.error(request, "Error fetching inventory.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching inventory."},
                status=500,
            )


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
                    inventory = form.save()
                    inventory.product.inside_inventory = True
                    inventory.product.save()
                messages.success(request, "Inventory created successfully.")
                return redirect("inventory_list")

            messages.error(request, "Invalid inventory form.")
            return render(
                request, "vendor/inventory/inventory_form.html", {"form": form}
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error creating inventory.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error creating inventory."},
                status=500,
            )


class InventoryUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, pk, *args, **kwargs):
        try:
            inventory = get_object_or_404(Inventory, pk=pk, is_deleted=False)
            form = InventoryForm(instance=inventory, user=request.user)
            return render(
                request,
                "vendor/inventory/inventory_form.html",
                {"form": form, "inventory": inventory},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching inventory.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching inventory."},
                status=500,
            )

    def post(self, request, pk, *args, **kwargs):
        try:
            inventory = get_object_or_404(Inventory, pk=pk, is_deleted=False)
            form = InventoryForm(request.POST, instance=inventory, user=request.user)

            if form.is_valid():
                with transaction.atomic():
                    inventory = form.save()
                    inventory.product.inside_inventory = True
                    inventory.product.save()
                messages.success(request, "Inventory updated successfully.")
                return redirect("inventory_list")

            messages.error(request, "Invalid inventory form.")
            return render(
                request,
                "vendor/inventory/inventory_form.html",
                {"form": form, "inventory": inventory},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error updating inventory.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error updating inventory."},
                status=500,
            )


class InventoryBulkCatalogUpdateView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, *args, **kwargs):
        try:
            ids = request.POST.getlist("inventory_ids")
            action = request.POST.get("action")

            if not ids or action not in ["add", "remove", "delete"]:
                messages.error(request, "Invalid selection or action.")
                return redirect("inventory_list")

            inventories = Inventory.objects.filter(
                id__in=ids, is_deleted=False, company__owner__user=request.user
            )

            if action == "delete":
                for each in inventories:
                    each.product.inside_inventory = False
                    each.product.save()
                    each.is_deleted = True
                    each.save()
            else:
                update_value = action == "add"
                inventories.update(catalog_display=update_value)

            messages.success(
                request, f"Inventory action '{action}' executed successfully."
            )
            return redirect("inventory_list")

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error performing inventory action.")
            return redirect("inventory_list")


class CatalogProductDetailView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, inventory_id, *args, **kwargs):
        try:
            inventory = get_object_or_404(Inventory, pk=inventory_id, is_deleted=False)
            context = {
                "product": inventory.product.name,
                "description": inventory.product.description,
                "category": inventory.product.category.name,
                "price": inventory.price,
                "stock": inventory.stock,
                "product_imgs": ProductImage.objects.filter(
                    product=inventory.product, is_deleted=False
                ),
                "product_single_img": ProductImage.objects.filter(
                    product=inventory.product, is_deleted=False
                ).first(),
                "company": inventory.company.name,
                "company_id": inventory.company.pk,
                "product_id": inventory.product.pk,
                "inventory_id": inventory.pk,
            }
            return render(
                request,
                "vendor/catalog/catalog_detail_view.html",
                context,
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching product details.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching product details."},
                status=500,
            )
