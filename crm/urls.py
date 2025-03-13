from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Public Landing Page
    path("", include("landing.urls")),

    # User Authentication & Profile Management
    path("user/", include("users.urls")),

    # Dynamic URLs Based on Company Name
    path("<str:name>/", include("company_admin.urls")),  # CRM Dashboard for Each Company

] + debug_toolbar_urls()
