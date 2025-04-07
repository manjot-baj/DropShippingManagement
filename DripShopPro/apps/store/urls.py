from django.urls import path
from store.Views.store_views import (
    StoreView,
    StoreCreateView,
    StoreUpdateView,
    StoreDeleteView,
)

urlpatterns = [
    # Store URLs
    path("store/", StoreView.as_view(), name="store_view"),
    path("store/create/", StoreCreateView.as_view(), name="store_create"),
    path("store/<int:pk>/update/", StoreUpdateView.as_view(), name="store_update"),
    path("store/<int:pk>/delete/", StoreDeleteView.as_view(), name="store_delete"),
]
