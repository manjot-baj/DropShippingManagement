import logging
import traceback
from django.views import View
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user_profile.middlewares import RoleRequiredMixin
from store.Utils.middlewares import StoreRequiredMixin
from catalog.models import Company, Inventory, ProductImage
from store.models import Store, StoreProduct

logger = logging.getLogger("error_log")


# List all Vendors (for Merchant)
class VendorListView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        try:
            vendors = Company.objects.select_related("owner").filter(is_deleted=False)
            return render(
                request,
                "merchant/vendor_catalog/vendor_list.html",
                {"vendors": vendors},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching vendors.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching company."},
                status=500,
            )


# Vendor Catalogs
class VendorCatalogView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, company_id, *args, **kwargs):
        try:
            store = get_object_or_404(Store, owner__user=request.user)
            company = get_object_or_404(
                Company,
                pk=company_id,
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
                        "product_id": inventory.product.pk,
                        "inventory_id": inventory.pk,
                        "store_id": store.pk,
                        "in_store": StoreProduct.objects.filter(
                            store=store, inventory=inventory
                        ).exists(),
                    }
                )
            return render(
                request,
                "merchant/vendor_catalog/catalog.html",
                {
                    "catalogs": catalogs,
                    "company": company,
                },
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching vendor catalogs.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching catalogs."},
                status=500,
            )


# Product Detail View
class VendorCatalogProductDetailView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

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
                "company": inventory.company,
                "product_id": inventory.product.pk,
                "inventory_id": inventory.pk,
            }
            return render(
                request,
                "merchant/vendor_catalog/catalog_detail_view.html",
                context,
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching product details.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching product details."},
                status=500,
            )
