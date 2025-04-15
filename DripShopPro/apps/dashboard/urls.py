from django.urls import path
from dashboard.views import (
    VendorDashboardView,
    MerchantDashboardView,
    CustomerDashboardView,
)

urlpatterns = [
    path("vendor/", VendorDashboardView.as_view(), name="vendor_dashboard"),
    path("merchant/", MerchantDashboardView.as_view(), name="merchant_dashboard"),
    path("customer/", CustomerDashboardView.as_view(), name="customer_dashboard"),
]
