import logging
import traceback
from django.shortcuts import render
from user_profile.models import UserProfile
from catalog.models import Category
from user_profile.middlewares import RoleRequiredMixin
from django.views import View
from django.contrib import messages
from store.models import StoreProduct
from catalog.models import ProductImage

logger = logging.getLogger("error_log")


class VendorDashboardView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            return render(request, f"vendor/dashboard.html", {"user": user})
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )


class MerchantDashboardView(RoleRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            return render(request, f"merchant/dashboard.html", {"user": user})
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )


class CustomerDashboardView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            categorys = Category.objects.all()
            store_products = StoreProduct.objects.filter(is_deleted=False)
            products = []
            for store_product in store_products:
                cost_price = float(store_product.inventory.price)
                margin_price = float(cost_price * (int(store_product.margin) / 100))
                selling_price = cost_price + margin_price
                data = {
                    "name": store_product.inventory.product.name,
                    "category": store_product.inventory.product.category.name,
                    "description": store_product.inventory.product.description,
                    "price": selling_price,
                    "stock": store_product.inventory.stock,
                    "main_img": ProductImage.objects.filter(
                        product=store_product.inventory.product,
                        is_deleted=False,
                    ).latest("pk"),
                    "imgs": ProductImage.objects.filter(
                        product=store_product.inventory.product,
                        is_deleted=False,
                    ),
                }
                products.append(data)
            return render(
                request,
                f"customer/dashboard.html",
                {"user": user, "categorys": categorys, "products": products},
            )
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "customer/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )
