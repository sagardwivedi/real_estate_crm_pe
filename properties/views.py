from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from leads.views import GroupRequiredMixin

from .models import Property


class PropertyListView(GroupRequiredMixin, ListView):
    model = Property
    template_name = "property_list.html"
    context_object_name = "properties"
    required_groups = ["Company Admin", "Sales Manager", "Agent"]


class PropertyDetailView(GroupRequiredMixin, DetailView):
    model = Property
    template_name = "property_detail.html"
    context_object_name = "property"


class PropertyCreateView(GroupRequiredMixin, CreateView):
    model = Property
    fields = ["title", "address", "price"]
    template_name = "property_form.html"
    required_groups = ["Company Admin"]

    def get_success_url(self):
        return reverse_lazy(
            "properties:property_list", kwargs={"name": self.kwargs["name"]}
        )


class PropertyDeleteView(GroupRequiredMixin, DeleteView):
    model = Property
    template_name = "property_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "properties:property_list", kwargs={"name": self.kwargs["name"]}
        )
