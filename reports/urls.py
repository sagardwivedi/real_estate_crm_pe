from django.urls import path

from .views import ExportReportCSVView, ReportDashboardView

app_name = "reports"

urlpatterns = [
    path("", ReportDashboardView.as_view(), name="dashboard"),
    path("export/csv/", ExportReportCSVView.as_view(), name="export_csv"),
]
