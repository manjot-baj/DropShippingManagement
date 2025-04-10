import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from user_profile.middlewares import RoleRequiredMixin
from store.models import Store, StoreProduct
from store.Forms.store_forms import StoreForm
from user_profile.models import UserProfile
from catalog.models import Company, Inventory, ProductImage
from store.Utils.middlewares import StoreRequiredMixin

logger = logging.getLogger("error_log")


class StoreView(RoleRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        try:
            store_obj = (
                Store.objects.select_related("owner")
                .filter(
                    owner__user=request.user,
                    is_deleted=False,
                )
                .first()
            )

            products = []
            store_product_objs = StoreProduct.objects.filter(store=store_obj)
            for store_product in store_product_objs:
                cost_price = store_product.inventory.price
                margin_price = cost_price * int(store_product.margin)
                selling_price = cost_price + (margin_price / 100)
                products.append(
                    {
                        "product": store_product.inventory.product.name,
                        "description": store_product.inventory.product.description,
                        "category": store_product.inventory.product.category.name,
                        "selling_price": selling_price,
                        "cost_price": cost_price,
                        "stock": store_product.inventory.stock,
                        "product_imgs": ProductImage.objects.filter(
                            product=store_product.inventory.product, is_deleted=False
                        ),
                        "product_single_img": ProductImage.objects.filter(
                            product=store_product.inventory.product, is_deleted=False
                        ).first(),
                        "inventory_id": store_product.inventory.pk,
                        "store_product_id": store_product.pk,
                        "margin": int(store_product.margin),
                    }
                )

            return render(
                request,
                "merchant/store/store_view.html",
                {"store": store_obj, "products": products},
            )
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


# Add or Update Products to Store
class StoreProductCreateOrUpdateView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def post(self, request, store_id, inventory_id, *args, **kwargs):
        try:
            margin = request.POST.get("margin", 5)
            store = Store.objects.get(id=store_id)
            inventory = Inventory.objects.get(id=inventory_id)
            sp = None
            action = None
            with transaction.atomic():
                if StoreProduct.objects.filter(
                    store=store,
                    inventory=inventory,
                ).exists():
                    sp = StoreProduct.objects.filter(
                        store=store, inventory=inventory
                    ).latest("pk")
                    print(int(margin))
                    sp.margin = int(margin)
                    sp.save()
                    action = "Update"
                else:
                    sp = StoreProduct(
                        store=store, inventory=inventory, margin=int(margin)
                    )
                    sp.save()
                    action = "Create"

            if action == "Create":
                messages.success(request, "Product Added to Store successfully.")
                return redirect(
                    "vendor_catalog_view", company_id=sp.inventory.company.pk
                )

            if action == "Update":
                messages.success(request, "Store Product Margin Updated successfully.")
                return redirect("store_view")

        except:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while adding or updating product to store.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error while adding or updating product to store."},
                status=500,
            )


# Store Product Detail View
class StoreProductDetailView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, inventory_id, *args, **kwargs):
        try:
            inventory = get_object_or_404(Inventory, pk=inventory_id, is_deleted=False)
            store_product = StoreProduct.objects.filter(inventory=inventory).latest(
                "pk"
            )
            store = store_product.store
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
                "inventory_id": inventory.pk,
                "store": store,
                "store_product_id": store_product.pk,
            }

            margin = store_product.margin
            cost_price = store_product.inventory.price
            margin_price = cost_price * int(store_product.margin)
            selling_price = cost_price + (margin_price / 100)

            context["selling_price"] = selling_price
            context["cost_price"] = cost_price
            context["margin"] = margin

            return render(
                request,
                "merchant/store/store_product_detail_view.html",
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


class StoreProductDeleteView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def post(self, request, store_product_id, *args, **kwargs):
        try:
            store = get_object_or_404(StoreProduct, pk=store_product_id)
            store.delete()
            messages.success(request, "Product removed from Store successfully.")
            return JsonResponse(
                {"success": True, "message": "Product removed from Store successfully."}
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error removing product from store.")
            return JsonResponse(
                {"success": False, "message": "Error removing product from store."},
                status=500,
            )
