from django.urls import path
from catalog.Views.product_views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductImageDeleteView,
)
from catalog.Views.company_views import (
    CompanyListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
)
from catalog.Views.inventory_views import (
    InventoryListView,
    InventoryCreateView,
    InventoryUpdateView,
    InventoryBulkCatalogUpdateView,
    CompanyProductCatalogView,
    CatalogProductDetailView,
)

from catalog.Views.merchant_views import MerchantListView
from catalog.Views.invoice_views import VendorInvoiceView

urlpatterns = [
    # Product URLs
    path(
        "products/image/<int:image_id>/delete/",
        ProductImageDeleteView.as_view(),
        name="product_image_delete",
    ),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("products/merchant_list/", MerchantListView.as_view(), name="merchant_list"),
    # Company URLs
    path("company/", CompanyListView.as_view(), name="company_list"),
    path("company/create/", CompanyCreateView.as_view(), name="company_create"),
    path(
        "company/<int:pk>/update/", CompanyUpdateView.as_view(), name="company_update"
    ),
    path(
        "company/<int:pk>/delete/", CompanyDeleteView.as_view(), name="company_delete"
    ),
    # Catalog URLs
    path(
        "catalog/<int:company_id>/view",
        CompanyProductCatalogView.as_view(),
        name="catalog_view",
    ),
    path(
        "catalog/<int:inventory_id>/product_detail",
        CatalogProductDetailView.as_view(),
        name="catalog_product_detail_view",
    ),
    # Inventory URLs
    path("inventory/", InventoryListView.as_view(), name="inventory_list"),
    path("inventory/create/", InventoryCreateView.as_view(), name="inventory_create"),
    path(
        "inventory/<int:pk>/update/",
        InventoryUpdateView.as_view(),
        name="inventory_update",
    ),
    path(
        "inventory/bulk-catalog-update/",
        InventoryBulkCatalogUpdateView.as_view(),
        name="inventory_bulk_catalog_update",
    ),
    path(
        "invoice/",
        VendorInvoiceView.as_view(),
        name="invoice",
    ),
]
