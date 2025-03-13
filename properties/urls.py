from django.urls import path

from .views import (
    PropertyCreateView,
    PropertyDeleteView,
    PropertyDetailView,
    PropertyListView,
)

app_name = "properties"

urlpatterns = [
    path("", PropertyListView.as_view(), name="property_list"),
    path(
        "<int:pk>/",
        PropertyDetailView.as_view(),
        name="property_detail",
    ),
    path(
        "add/",
        PropertyCreateView.as_view(),
        name="property_create",
    ),
    path(
        "<int:pk>/delete/",
        PropertyDeleteView.as_view(),
        name="property_delete",
    ),
]
