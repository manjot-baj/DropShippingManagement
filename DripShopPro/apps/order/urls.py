from django.urls import path
from order.views import (
    CustomerProductDetailView,
    WishlistProductListView,
    AddProductToWishlistView,
    DeleteProductFromWishlistView,
    CartProductListView,
    AddProductToCartView,
    DeleteProductFromCartView,
    AddProductQtyToCartView,
    OrderCreateView,
    OrderListView,
)

urlpatterns = [
    # customer Product detail view
    path(
        "customer_product_detail/<int:product_id>/",
        CustomerProductDetailView.as_view(),
        name="customer_product_detail",
    ),
    # Wishlist
    path("wishlist/", WishlistProductListView.as_view(), name="wishlist"),
    path(
        "add_to_wishlist/<int:product_id>/",
        AddProductToWishlistView.as_view(),
        name="add_to_wishlist",
    ),
    path(
        "remove_from_wishlist/<int:wishlist_item_id>/",
        DeleteProductFromWishlistView.as_view(),
        name="remove_from_wishlist",
    ),
    # Cart
    path("cart/", CartProductListView.as_view(), name="cart"),
    path(
        "add_to_cart/<int:product_id>/",
        AddProductToCartView.as_view(),
        name="add_to_cart",
    ),
    path(
        "remove_from_cart/<int:cart_item_id>/",
        DeleteProductFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path(
        "add_qty_to_cart_product/<int:cart_item_id>/",
        AddProductQtyToCartView.as_view(),
        name="add_qty_to_cart_product",
    ),
    path(
        "checkout/",
        OrderCreateView.as_view(),
        name="checkout",
    ),
    path(
        "create_order/",
        OrderCreateView.as_view(),
        name="create_order",
    ),
    path(
        "order/",
        OrderListView.as_view(),
        name="order",
    ),
]
