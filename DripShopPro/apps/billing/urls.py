from django.urls import path
from billing.views import (
    CreatePurchaseOrderView,
    MerchantPurchaseOrderListView,
    MerchantPODetailView,
    VendorPODetailView,
    VendorPurchaseOrderListView,
)

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
    path(
        "merchant_po_detail/<int:po_id>/",
        MerchantPODetailView.as_view(),
        name="merchant_po_detail",
    ),
    path(
        "vendor_purchase_order_list/",
        VendorPurchaseOrderListView.as_view(),
        name="vendor_purchase_order_list",
    ),
    path(
        "vendor_po_detail/<int:po_id>/",
        VendorPODetailView.as_view(),
        name="vendor_po_detail",
    ),
]
