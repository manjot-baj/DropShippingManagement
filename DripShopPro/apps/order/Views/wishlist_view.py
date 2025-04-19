import logging
import traceback
from django.shortcuts import render, get_object_or_404, redirect
from user_profile.middlewares import RoleRequiredMixin
from django.views import View
from django.contrib import messages
from order.models import WishList, Cart
from catalog.models import ProductImage
from store.models import StoreProduct
from user_profile.models import UserProfile

logger = logging.getLogger("error_log")


class WishlistProductListView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            wishlist_products = WishList.objects.filter(
                is_deleted=False, owner__user=request.user
            )

            products = []
            for wishlist_product in wishlist_products:
                cost_price = float(wishlist_product.product.inventory.price)
                margin_price = float(
                    cost_price * (int(wishlist_product.product.margin) / 100)
                )
                selling_price = cost_price + margin_price

                data = {
                    "name": wishlist_product.product.inventory.product.name,
                    "category": wishlist_product.product.inventory.product.category.name,
                    "description": wishlist_product.product.inventory.product.description,
                    "price": selling_price,
                    "stock": wishlist_product.product.inventory.stock,
                    "main_img": ProductImage.objects.filter(
                        product=wishlist_product.product.inventory.product,
                        is_deleted=False,
                    ).latest("pk"),
                    "imgs": ProductImage.objects.filter(
                        product=wishlist_product.product.inventory.product,
                        is_deleted=False,
                    ),
                    "product_id": wishlist_product.product.pk,
                    "wishlist_item_id": wishlist_product.pk,
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


class AddProductToWishlistView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, product_id, *args, **kwargs):
        try:
            product = get_object_or_404(
                StoreProduct,
                pk=product_id,
                is_deleted=False,
            )
            owner = get_object_or_404(UserProfile, user=request.user)
            if Cart.objects.filter(product=product, owner=owner).exists():
                Cart.objects.get(product=product, owner=owner).delete()
            WishList.objects.update_or_create(product=product, owner=owner)
            messages.success(request, "Product Added to WishList")
            return redirect("wishlist")
        except:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while adding Product to WishList")
            return render(
                request,
                "customer/error.html",
                {"message": "Error fetching products."},
                status=500,
            )


class DeleteProductFromWishlistView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, wishlist_item_id, *args, **kwargs):
        try:
            wishlist_item = WishList.objects.get(pk=wishlist_item_id)
            wishlist_item.delete()
            messages.success(request, "Product Removed from WishList")
            return redirect("wishlist")
        except:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while Removing Product from WishList")
            return render(
                request,
                "customer/error.html",
                {"message": "Error fetching products."},
                status=500,
            )
