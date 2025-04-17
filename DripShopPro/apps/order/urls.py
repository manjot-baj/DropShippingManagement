from django.urls import path
from order.views import CustomerProductDetailView

urlpatterns = [
    path("customer_product_detail/<int:product_id>/", CustomerProductDetailView.as_view(), name="customer_product_detail"),
]
