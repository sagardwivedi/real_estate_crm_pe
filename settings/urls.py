from django.urls import path

from .views import (
    CompanyEditView,
    CompanyView,
    SubscriptionView,
    UserManagementView,
)

app_name = "company_settings"

urlpatterns = [
    path("company/", CompanyView.as_view(), name="company_view"),  # Read-only view
    path("company/edit/", CompanyEditView.as_view(), name="company_edit"),  # Edit view
    path("user-management/", UserManagementView.as_view(), name="user_management"),
    path("subscription/", SubscriptionView.as_view(), name="subscription"),
]
