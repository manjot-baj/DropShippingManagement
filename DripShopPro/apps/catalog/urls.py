from django.urls import path
from catalog.Views.product_views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductImageDeleteView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

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
    # Category URLs
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path(
        "category/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),
]
