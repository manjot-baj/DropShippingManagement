import logging
import traceback
from django.shortcuts import render
from user_profile.models import UserProfile
from user_profile.middlewares import RoleRequiredMixin
from django.views import View
from django.contrib import messages
from store.models import StoreProduct
from catalog.models import Category, ProductImage
from order.models import Cart

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

            # Extract filter params
            category_filter = request.GET.get("category")
            name_filter = request.GET.get("name")
            price_min = request.GET.get("price_min")
            price_max = request.GET.get("price_max")

            # Base queryset
            store_products = StoreProduct.objects.filter(is_deleted=False)

            # Apply category filter
            if category_filter:
                store_products = store_products.filter(
                    inventory__product__category__name=category_filter
                )

            # Apply name filter
            if name_filter:
                store_products = store_products.filter(
                    inventory__product__name__icontains=name_filter
                )

            products = []
            for store_product in store_products:
                cost_price = float(store_product.inventory.price)
                margin_price = float(cost_price * (int(store_product.margin) / 100))
                selling_price = cost_price + margin_price

                # Apply price filter
                if price_min and selling_price < float(price_min):
                    continue
                if price_max and selling_price > float(price_max):
                    continue

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
                    "product_id": store_product.pk,
                }
                products.append(data)

            cart_item_count = Cart.objects.filter(
                is_deleted=False, owner__user=request.user
            ).count()
            return render(
                request,
                "customer/dashboard.html",
                {
                    "user": user,
                    "categorys": categorys,
                    "products": products,
                    "selected_category": category_filter,
                    "searched_name": name_filter,
                    "price_min": price_min,
                    "price_max": price_max,
                    "cart_item_count": cart_item_count,
                },
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching products.")
            return render(
                request,
                "customer/error.html",
                {"message": "Error fetching products."},
                status=500,
            )
