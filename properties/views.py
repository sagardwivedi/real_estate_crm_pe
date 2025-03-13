from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .models import Property


# Mixin to restrict access to Admins
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == "admin"


# Property List View
class PropertyListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Property
    template_name = "property_list.html"
    context_object_name = "properties"


# Property Detail View
class PropertyDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Property
    template_name = "property_detail.html"
    context_object_name = "property"


# Property Create View
class PropertyCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Property
    fields = ["name", "location", "price", "status", "description"]
    template_name = "property_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "properties:property_list", kwargs={"name": self.kwargs["name"]}
        )


# Property Delete View
class PropertyDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Property
    template_name = "property_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "properties:property_list", kwargs={"name": self.kwargs["name"]}
        )
