from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import LeadForm
from .models import Lead


class GroupRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to restrict access based on user groups."""

    required_groups = []  # List of groups allowed access

    def test_func(self):
        """Allow superusers OR users in the required group(s)."""
        user = self.request.user
        if user.is_superuser:  # Allow superusers to access everything
            return True
        return user.groups.filter(name__in=self.required_groups).exists()

    def handle_no_permission(self):
        """Raise a 403 error if access is denied."""
        raise PermissionDenied("You do not have permission to access this resource.")


class LeadListView(GroupRequiredMixin, ListView):
    model = Lead
    template_name = "lead_list.html"
    context_object_name = "leads"
    required_groups = ["Company Admin", "Sales Manager", "Agent"]


class LeadDetailView(GroupRequiredMixin, DetailView):
    model = Lead
    template_name = "lead_detail.html"
    context_object_name = "lead"
    required_groups = ["Company Admin", "Sales Manager", "Agent"]


class LeadCreateView(GroupRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = "lead_form.html"
    success_url = reverse_lazy("leads:lead_list")
    required_groups = ["Company Admin", "Sales Manager", "Agent"]


class LeadDeleteView(GroupRequiredMixin, DeleteView):
    model = Lead
    template_name = "lead_confirm_delete.html"
    success_url = reverse_lazy("leads:lead_list")
    required_groups = ["Company Admin"]
