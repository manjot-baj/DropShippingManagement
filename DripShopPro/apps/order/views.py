import random
import string
import logging
import traceback
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from user_profile.middlewares import RoleRequiredMixin
from django.views import View
from django.contrib import messages
from store.models import StoreProduct
from catalog.models import ProductImage
from order.models import Cart, WishList, Order, OrderItem
from user_profile.models import UserProfile
from order.forms import OrderForm

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


class CartProductListView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            cart_products = Cart.objects.filter(
                is_deleted=False, owner__user=request.user
            )

            products = []
            grand_total = 0
            for cart_product in cart_products:
                cost_price = float(cart_product.product.inventory.price)
                margin_price = float(
                    cost_price * (int(cart_product.product.margin) / 100)
                )
                selling_price = cost_price + margin_price
                total_amount = selling_price * int(cart_product.quantity)
                grand_total = grand_total + total_amount
                data = {
                    "name": cart_product.product.inventory.product.name,
                    "category": cart_product.product.inventory.product.category.name,
                    "description": cart_product.product.inventory.product.description,
                    "price": selling_price,
                    "total_amount": total_amount,
                    "stock": cart_product.product.inventory.stock,
                    "main_img": ProductImage.objects.filter(
                        product=cart_product.product.inventory.product,
                        is_deleted=False,
                    ).latest("pk"),
                    "imgs": ProductImage.objects.filter(
                        product=cart_product.product.inventory.product,
                        is_deleted=False,
                    ),
                    "quantity": cart_product.quantity,
                    "product_id": cart_product.product.pk,
                    "cart_item_id": cart_product.pk,
                }
                products.append(data)

            return render(
                request,
                "customer/cart.html",
                {
                    "products": products,
                    "total": grand_total,
                    "count": cart_products.count(),
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


class AddProductQtyToCartView(RoleRequiredMixin, View):
    required_role = "Customer"

    def post(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = Cart.objects.get(pk=cart_item_id)
            qty = request.POST.get("qty")
            cart_item.quantity = int(qty)
            cart_item.save()
            messages.success(request, "Product Qty added to Cart")
            return redirect("cart")
        except:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while adding Product Qty to Cart")
            return render(
                request,
                "customer/error.html",
                {"message": "Error while adding Product Qty to Cart"},
                status=500,
            )


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


def generate_order_id(length=12):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


class OrderCreateView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        form = OrderForm(user=request.user)
        cart_products = Cart.objects.filter(is_deleted=False, owner__user=request.user)

        products = []
        grand_total = 0
        for cart_product in cart_products:
            cost_price = float(cart_product.product.inventory.price)
            margin_price = float(cost_price * (int(cart_product.product.margin) / 100))
            selling_price = cost_price + margin_price
            total_amount = selling_price * int(cart_product.quantity)
            grand_total = grand_total + total_amount
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
                "total_amount": total_amount,
                "quantity": cart_product.quantity,
            }
            products.append(data)
        return render(
            request,
            "customer/checkout.html",
            {
                "form": form,
                "products": products,
                "grand_total": grand_total,
                "count": cart_products.count(),
            },
        )

    def post(self, request, *args, **kwargs):
        try:
            form = OrderForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.owner = get_object_or_404(UserProfile, user=request.user)
                    order_id = None
                    while True:
                        order_id = generate_order_id()
                        if not Order.objects.filter(order_id=order_id).exists():
                            break
                    order.order_id = order_id
                    order.save()

                    cart_products = Cart.objects.filter(
                        is_deleted=False, owner__user=request.user
                    )
                    grand_total = 0
                    for cart_product in cart_products:
                        cost_price = float(cart_product.product.inventory.price)
                        margin_price = float(
                            cost_price * (int(cart_product.product.margin) / 100)
                        )
                        selling_price = cost_price + margin_price
                        total = selling_price * int(cart_product.quantity)
                        grand_total = grand_total + total

                        if not OrderItem.objects.filter(
                            parent=order,
                            product=cart_product.product,
                            store_price=selling_price,
                            vendor_price=cost_price,
                            merchant_margin_price=margin_price,
                            merchant_margin=int(cart_product.product.margin),
                            quantity=cart_product.quantity,
                            total_amount=total,
                        ).exists():
                            order_item = OrderItem(
                                parent=order,
                                product=cart_product.product,
                                store_price=selling_price,
                                vendor_price=cost_price,
                                merchant_margin_price=margin_price,
                                merchant_margin=int(cart_product.product.margin),
                                quantity=cart_product.quantity,
                                total_amount=total,
                            )
                            order_item.save()
                            cart_product.delete()
                    order.grand_total = float(grand_total)
                    order.save()
                messages.success(request, "Order Placed.")
                return redirect("order")
            messages.error(request, "Invalid order form.")
            return redirect("checkout")
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error creating Order.")
            return render(
                request,
                "customer/error.html",
                {"message": "Error creating Order."},
                status=500,
            )


class OrderListView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            order_data = []
            orders = Order.objects.filter(is_deleted=False, owner__user=request.user)
            for order in orders:
                order_items = OrderItem.objects.filter(parent=order)
                products = []
                for order_item in order_items:
                    total_amount = float(order_item.total_amount)
                    products.append(
                        {
                            "name": order_item.product.inventory.product.name,
                            "quantity": int(order_item.quantity),
                            "total_amount": total_amount,
                            "price": order_item.store_price,
                            "main_img": ProductImage.objects.filter(
                                product=order_item.product.inventory.product,
                                is_deleted=False,
                            ).latest("pk"),
                            "status": order_item.status,
                            "order_item_id": order_item.pk,
                            "confirmed_date": (
                                str(order_item.confirmed_date.date())
                                if order_item.confirmed_date
                                else None
                            ),
                            "shipping_date": (
                                str(order_item.shipping_date.date())
                                if order_item.shipping_date
                                else None
                            ),
                            "arrival_date": (
                                str(order_item.arrival_date.date())
                                if order_item.arrival_date
                                else None
                            ),
                            "delivery_date": (
                                str(order_item.delivery_date.date())
                                if order_item.delivery_date
                                else None
                            ),
                        }
                    )
                order_data.append(
                    {
                        "order_date": str(order.created_at.date()),
                        "order_id": order.pk,
                        "order_no": order.order_id,
                        "grand_total": float(order.grand_total),
                        "products": products,
                    }
                )
            return render(
                request,
                "customer/order.html",
                {
                    "order_data": order_data,
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


class OrderSummaryView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
            order_items = OrderItem.objects.filter(parent=order)
            products = []
            for order_item in order_items:
                total_amount = float(order_item.total_amount)
                products.append(
                    {
                        "name": order_item.product.inventory.product.name,
                        "quantity": int(order_item.quantity),
                        "total_amount": total_amount,
                        "price": order_item.store_price,
                        "main_img": ProductImage.objects.filter(
                            product=order_item.product.inventory.product,
                            is_deleted=False,
                        ).latest("pk"),
                        "status": order_item.status,
                        "order_item_id": order_item.pk,
                        "confirmed_date": (
                            str(order_item.confirmed_date.date())
                            if order_item.confirmed_date
                            else None
                        ),
                        "shipping_date": (
                            str(order_item.shipping_date.date())
                            if order_item.shipping_date
                            else None
                        ),
                        "arrival_date": (
                            str(order_item.arrival_date.date())
                            if order_item.arrival_date
                            else None
                        ),
                        "delivery_date": (
                            str(order_item.delivery_date.date())
                            if order_item.delivery_date
                            else None
                        ),
                    }
                )
                order_data = {
                    "order_date": str(order.created_at.date()),
                    "order_id": order.pk,
                    "order_no": order.order_id,
                    "grand_total": float(order.grand_total),
                    "products": products,
                    "address": order.address,
                    "city": order.city,
                    "state": order.state,
                    "postal_code": order.postal_code,
                    "country": order.country,
                    "item_count": order_items.count(),
                }
            return render(
                request,
                "customer/order_summary.html",
                {
                    "order_data": order_data,
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
