from django.urls import path
from catalog.Views.product_views import (
    product_list,
    product_create,
    product_update,
    product_delete,
    product_image_delete,
)

# from catalog.Views.catalog_views import (
#     catalog_detail,
#     catalog_create,
#     catalog_update,
#     catalog_delete,
# )

urlpatterns = [
    # Product URLs
    path("products/", product_list, name="product_list"),
    path("products/new/", product_create, name="product_create"),
    path("products/<int:pk>/edit/", product_update, name="product_update"),
    path("products/<int:pk>/delete/", product_delete, name="product_delete"),
    path(
        "products/image/<int:pk>/delete/",
        product_image_delete,
        name="product_image_delete",
    ),
    # catalog URLS
    # path("catalog/", catalog_detail, name="catalog_detail"),
    # path("catalog/new/", catalog_create, name="catalog_create"),
    # path("catalog/edit/", catalog_update, name="catalog_update"),
    # path("catalog/delete/", catalog_delete, name="catalog_delete"),
]
