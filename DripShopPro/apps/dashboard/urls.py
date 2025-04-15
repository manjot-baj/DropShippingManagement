from django.urls import path
from dashboard.views import (
    VendorDashboardView,
    MerchantDashboardView,
    CustomerDashboardView,
)

urlpatterns = [
    path("vendor_dashboard/", VendorDashboardView.as_view(), name="vendor_dashboard"),
    path("merchant_dashboard/", MerchantDashboardView.as_view(), name="merchant_dashboard"),
    path("customer_dashboard/", CustomerDashboardView.as_view(), name="customer_dashboard"),
]
