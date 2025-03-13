from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing.urls")),
    path("user/", include("users.urls")),
    path("<str:name>/", include("company_admin.urls")),
    path("<str:name>/leads/", include("leads.urls")),
    path("<str:name>/properties/", include("properties.urls")),
    path("<str:name>/settings/", include("settings.urls")),
] + debug_toolbar_urls()
