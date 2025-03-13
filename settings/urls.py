from django.urls import path

from .views import CompanyInfoView, SecurityView, SubscriptionView, UserManagementView

app_name = "company_settings"

urlpatterns = [
    path("company-info/", CompanyInfoView.as_view(), name="company_info"),
    path("user-management/", UserManagementView.as_view(), name="user_management"),
    path("subscription/", SubscriptionView.as_view(), name="subscription"),
    path("security/", SecurityView.as_view(), name="security"),
]
