from django.urls import path
from catalog.Views.product_views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductImageDeleteView,
)

# from catalog.Views.catalog_views import (
#     catalog_detail,
#     catalog_create,
#     catalog_update,
#     catalog_delete,
# )

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
    # catalog URLS
    # path("catalog/", catalog_detail, name="catalog_detail"),
    # path("catalog/new/", catalog_create, name="catalog_create"),
    # path("catalog/edit/", catalog_update, name="catalog_update"),
    # path("catalog/delete/", catalog_delete, name="catalog_delete"),
]
