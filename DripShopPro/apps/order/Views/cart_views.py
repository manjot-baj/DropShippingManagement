import logging
import traceback
from django.shortcuts import render, get_object_or_404, redirect
from user_profile.middlewares import RoleRequiredMixin
from django.views import View
from django.contrib import messages
from order.models import Cart, WishList
from catalog.models import ProductImage
from store.models import StoreProduct
from user_profile.models import UserProfile

logger = logging.getLogger("error_log")


class CartProductListView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            cart_products = Cart.objects.filter(
                is_deleted=False, owner__user=request.user
            )

            products = []
            total = 0
            for cart_product in cart_products:
                cost_price = float(cart_product.product.inventory.price)
                margin_price = float(
                    cost_price * (int(cart_product.product.margin) / 100)
                )
                selling_price = cost_price + margin_price
                total = total + selling_price
                data = {
                    "name": cart_product.product.inventory.product.name,
                    "category": cart_product.product.inventory.product.category.name,
                    "description": cart_product.product.inventory.product.description,
                    "price": selling_price,
                    "stock": cart_product.product.inventory.stock,
                    "main_img": ProductImage.objects.filter(
                        product=cart_product.product.inventory.product,
                        is_deleted=False,
                    ).latest("pk"),
                    "imgs": ProductImage.objects.filter(
                        product=cart_product.product.inventory.product,
                        is_deleted=False,
                    ),
                    "product_id": cart_product.product.pk,
                    "cart_item_id": cart_product.pk,
                }
                products.append(data)

            return render(
                request,
                "customer/cart.html",
                {"products": products, "total": total, "count": cart_products.count()},
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


class AddProductToCartView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, product_id, *args, **kwargs):
        try:
            product = get_object_or_404(
                StoreProduct,
                pk=product_id,
                is_deleted=False,
            )
            owner = get_object_or_404(UserProfile, user=request.user)
            if WishList.objects.filter(product=product, owner=owner).exists():
                WishList.objects.get(product=product, owner=owner).delete()
            Cart.objects.update_or_create(product=product, owner=owner)
            messages.success(request, "Product Added to Cart")
            return redirect("cart")
        except:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while adding Product to Cart")
            return render(
                request,
                "customer/error.html",
                {"message": "Error fetching products."},
                status=500,
            )


class DeleteProductFromCartView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = Cart.objects.get(pk=cart_item_id)
            cart_item.delete()
            messages.success(request, "Product Removed from Cart")
            return redirect("cart")
        except:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while Removing Product from Cart")
            return render(
                request,
                "customer/error.html",
                {"message": "Error fetching products."},
                status=500,
            )
