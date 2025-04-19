import logging
import traceback
from django.shortcuts import render, get_object_or_404
from user_profile.middlewares import RoleRequiredMixin
from django.views import View
from django.contrib import messages
from store.models import StoreProduct
from catalog.models import ProductImage
from order.models import Cart, WishList

logger = logging.getLogger("error_log")


class CustomerProductDetailView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, product_id, *args, **kwargs):
        try:
            store_product = get_object_or_404(
                StoreProduct, pk=product_id, is_deleted=False
            )
            in_cart = Cart.objects.filter(
                product=store_product, owner__user=request.user
            ).exists()
            in_wishlist = WishList.objects.filter(
                product=store_product, owner__user=request.user
            ).exists()

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
                "product_id": store_product.pk,
                "in_cart": in_cart,
                "in_wishlist": in_wishlist,
            }

            return render(
                request,
                "customer/product_detail.html",
                data,
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


class CustomerWishlistView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            # Base queryset
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
                    "product_id": store_product.pk,
                }
                products.append(data)

            return render(
                request,
                "customer/wishlist.html",
                {
                    "products": products,
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


class CustomerCartView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            # Base queryset
            store_products = StoreProduct.objects.filter(is_deleted=False)

            products = []
            total = 0
            for store_product in store_products:
                cost_price = float(store_product.inventory.price)
                margin_price = float(cost_price * (int(store_product.margin) / 100))
                selling_price = cost_price + margin_price
                total = total + selling_price
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

            return render(
                request,
                "customer/cart.html",
                {
                    "products": products,
                    "total": total,
                    "count": store_products.count(),
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


class CustomerOrderView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            # Base queryset
            store_products = StoreProduct.objects.filter(is_deleted=False)

            products = []
            total = 0
            for store_product in store_products:
                cost_price = float(store_product.inventory.price)
                margin_price = float(cost_price * (int(store_product.margin) / 100))
                selling_price = cost_price + margin_price
                total = total + selling_price
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

            return render(
                request,
                "customer/order.html",
                {
                    "products": products,
                    "total": total,
                    "count": store_products.count(),
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
