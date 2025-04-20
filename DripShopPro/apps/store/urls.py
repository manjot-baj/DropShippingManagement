from django.urls import path
from store.Views.store_views import (
    StoreView,
    StoreCreateView,
    StoreUpdateView,
    StoreDeleteView,
    StoreProductCreateOrUpdateView,
    StoreProductDetailView,
    StoreProductDeleteView,
    StoreProductListView,
    StoreVendorListView,
)
from store.Views.vendor_catalog_views import (
    VendorCatalogView,
    VendorListView,
    VendorCatalogProductDetailView,
)

urlpatterns = [
    # Store URLs
    path("store/", StoreView.as_view(), name="store_view"),
    path("store/create/", StoreCreateView.as_view(), name="store_create"),
    path("store/<int:pk>/update/", StoreUpdateView.as_view(), name="store_update"),
    path("store/<int:pk>/delete/", StoreDeleteView.as_view(), name="store_delete"),
    # Store Product
    # Add or Update
    path(
        "store/<int:store_id>/inventory/<int:inventory_id>/add_update_product/",
        StoreProductCreateOrUpdateView.as_view(),
        name="store_product_create_or_update",
    ),
    # Detail View
    path(
        "store/<int:inventory_id>/product_detail/",
        StoreProductDetailView.as_view(),
        name="store_product_detail_view",
    ),
    # Remove from store
    path(
        "store/<int:store_product_id>/delete/",
        StoreProductDeleteView.as_view(),
        name="remove_store_product",
    ),
    # List
    path("store_product/", StoreProductListView.as_view(), name="store_product_list"),
    # Store Vendors
    path("store_vendor/", StoreVendorListView.as_view(), name="store_vendor_list"),
    # Catalog
    path("vendor_list/", VendorListView.as_view(), name="vendor_list"),
    path(
        "vendor_catalog/<int:company_id>/view",
        VendorCatalogView.as_view(),
        name="vendor_catalog_view",
    ),
    path(
        "vendor_catalog/<int:inventory_id>/product_detail",
        VendorCatalogProductDetailView.as_view(),
        name="vendor_catalog_product_detail_view",
    ),
]
