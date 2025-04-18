from django.urls import path
from order.views import (
    CustomerProductDetailView,
    CustomerWishlistView,
    CustomerCartView,
    CustomerOrderView,
)

urlpatterns = [
    path(
        "customer_product_detail/<int:product_id>/",
        CustomerProductDetailView.as_view(),
        name="customer_product_detail",
    ),
    path("wishlist/", CustomerWishlistView.as_view(), name="wishlist"),
    path("cart/", CustomerCartView.as_view(), name="cart"),
    path("order/", CustomerOrderView.as_view(), name="order"),
]
