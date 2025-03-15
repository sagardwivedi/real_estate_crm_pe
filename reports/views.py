import csv
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView

from tenants.middleware import get_current_company
from transactions.models import Transaction
from users.models import CustomUser

from .forms import ReportFilterForm


class ReportDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "report_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_current_company()

        # Initialize the filter form with request GET parameters
        form = ReportFilterForm(self.request.GET)

        # Default date range: Last 30 days
        start_date = now() - timedelta(days=30)
        end_date = now()

        if form.is_valid():
            # Extract valid data from the form
            start_date = form.cleaned_data.get("start_date") or start_date
            end_date = form.cleaned_data.get("end_date") or end_date
            search_email = form.cleaned_data.get("email")

        # Filter Users
        user_query = Q()
        if search_email:
            user_query &= Q(email__icontains=search_email)

        total_users = CustomUser.objects.filter(user_query).count()
        active_users = CustomUser.objects.filter(
            user_query & Q(last_login__gte=start_date)
        ).count()

        # Filter Transactions
        transaction_query = Q(company=company, created_at__range=[start_date, end_date])

        total_transactions = Transaction.objects.filter(transaction_query).count()
        total_revenue = (
            Transaction.objects.filter(transaction_query).aggregate(
                total=Sum("sale_price")
            )["total"]
            or 0
        )

        context.update(
            {
                "form": form,
                "total_users": total_users,
                "active_users": active_users,
                "total_transactions": total_transactions,
                "total_revenue": total_revenue,
                "selected_start_date": start_date.strftime("%Y-%m-%d"),
                "selected_end_date": end_date.strftime("%Y-%m-%d"),
            }
        )
        return context


class ExportReportCSVView(LoginRequiredMixin, View):
    """View to export filtered report data as CSV."""

    def get(self, request, *args, **kwargs):
        company = request.user.company
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="company_report.csv"'

        writer = csv.writer(response)
        writer.writerow(["Metric", "Value"])

        # Get filter parameters
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        search_email = request.GET.get("email")

        # Default date range: Last 30 days
        if not start_date:
            start_date = now() - timedelta(days=30)
        else:
            start_date = now().strptime(start_date, "%Y-%m-%d").date()

        if not end_date:
            end_date = now().date()
        else:
            end_date = now().strptime(end_date, "%Y-%m-%d").date()

        # Filter Users
        user_query = models.Q()
        if search_email:
            user_query &= models.Q(email__icontains=search_email)

        total_users = CustomUser.objects.filter(user_query).count()
        active_users = CustomUser.objects.filter(
            user_query & models.Q(last_login__gte=start_date)
        ).count()

        # Filter Transactions
        transaction_query = models.Q(
            company=company, created_at__range=[start_date, end_date]
        )

        total_transactions = Transaction.objects.filter(transaction_query).count()
        total_revenue = (
            Transaction.objects.filter(transaction_query).aggregate(
                total=models.Sum("sale_price")
            )["total"]
            or 0
        )
        total_expenses = (
            Transaction.objects.filter(transaction_query).aggregate(
                total=models.Sum("sale_price")
            )["total"]
            or 0
        )

        # Write filtered data to CSV
        writer.writerow(["Total Users", total_users])
        writer.writerow(["Active Users (Last 30 days)", active_users])
        writer.writerow(["Total Transactions", total_transactions])
        writer.writerow(["Total Revenue ($)", f"{total_revenue:.2f}"])
        writer.writerow(["Total Expenses ($)", f"{total_expenses:.2f}"])

        return response
