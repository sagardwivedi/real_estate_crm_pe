from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from tenants.models import Company


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_slug = self.kwargs["name"]
        company = get_object_or_404(Company, name=company_slug)
        context["company"] = company
        return context
