from django.urls import path
from billing.views import CreatePurchaseOrderView, MerchantPurchaseOrderListView

urlpatterns = [
    path(
        "create_purchase_order/<int:order_item_id>/",
        CreatePurchaseOrderView.as_view(),
        name="create_purchase_order",
    ),
    path(
        "merchant_purchase_order_list/",
        MerchantPurchaseOrderListView.as_view(),
        name="merchant_purchase_order_list",
    ),
]
