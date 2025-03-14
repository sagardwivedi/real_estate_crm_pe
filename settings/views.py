from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from tenants.forms import CompanyForm
from tenants.models import Company
from users.models import CustomUser


class CompanyView(TemplateView):
    template_name = "company_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the company data associated with the current user
        context["company"] = self.request.user.company
        return context


class CompanyEditView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "company_edit.html"
    success_url = reverse_lazy("company_settings:company_view")

    def get_object(self):
        return self.request.user.company

    def form_valid(self, form):
        messages.success(self.request, "Company information updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the company information.",
        )
        return super().form_invalid(form)


# View for User Management section
class UserManagementView(TemplateView):
    template_name = "user_management.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = CustomUser.objects.all()
        return context


# View for Subscription section
class SubscriptionView(TemplateView):
    template_name = "subscription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.company
        context["subscription"] = company.subscription_plan
        return context
