from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from leads.forms import LeadForm

from .models import Lead


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == "admin"


class LeadListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Lead
    template_name = "lead_list.html"
    context_object_name = "leads"


class LeadDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Lead
    template_name = "lead_detail.html"
    context_object_name = "lead"


class LeadCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = "lead_form.html"
    success_url = reverse_lazy("leads:lead_list")


# Lead Delete View (Admins Only)
class LeadDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Lead
    template_name = "lead_confirm_delete.html"
    success_url = reverse_lazy("leads:lead_list")
