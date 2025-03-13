from django.urls import path

from .views import LeadCreateView, LeadDeleteView, LeadDetailView, LeadListView

app_name = "leads"

urlpatterns = [
    path("", LeadListView.as_view(), name="lead_list"),
    path("<int:pk>/", LeadDetailView.as_view(), name="lead_detail"),
    path("create/", LeadCreateView.as_view(), name="lead_create"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="lead_delete"),
]
