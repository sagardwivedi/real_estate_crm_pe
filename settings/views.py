from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from tenants.forms import CompanyForm
from tenants.models import Company
from users.models import CustomUser


# View for the Company Info section
class CompanyInfoView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "company_info.html"
    success_url = reverse_lazy("company_settings:company_info")

    def get_object(self):
        return self.request.user.company

    def form_valid(self, form):
        messages.success(self.request, "Company information updated successfully.")
        return super().form_valid(form)


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
        context["subscription"] = (
            company.subscription_plan
        )  # Assuming company has a subscription plan
        return context


# View for Security settings
class SecurityView(TemplateView):
    template_name = "security.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
