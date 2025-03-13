from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from leads.views import AdminRequiredMixin
from tenants.middleware import get_current_company
from users.forms import (
    AdminSignupForm,
    CompanySignupForm,
    CustomLoginForm,
    UserCreateForm,
    UserEditForm,
)
from users.models import CustomUser


class SignupView(TemplateView):
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        company_form = CompanySignupForm(request.POST)
        admin_form = AdminSignupForm(request.POST)

        if company_form.is_valid() and admin_form.is_valid():
            return self.form_valid(company_form, admin_form)

        messages.error(request, "Please correct the errors below.")
        return self.render_to_response(
            self.get_context_data(company_form=company_form, admin_form=admin_form)
        )

    def form_valid(self, company_form, admin_form):
        """Handles valid form submission by creating a company and an admin user."""
        company = company_form.save()
        admin_user = admin_form.save(commit=False)
        admin_user.company = company
        admin_user.role = "admin"
        admin_user.save()

        login(self.request, admin_user)
        messages.success(
            self.request, "Company and admin account created successfully!"
        )

        return redirect(reverse_lazy("dashboard", kwargs={"name": company.name}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault(
            "company_form", kwargs.get("company_form", CompanySignupForm())
        )
        context.setdefault("admin_form", kwargs.get("admin_form", AdminSignupForm()))
        return context


class CustomLoginView(LoginView):
    """Custom login view with improved redirection logic."""

    template_name = "login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated and user.company:
            return reverse_lazy("dashboard", kwargs={"name": user.company.name})
        return reverse_lazy("dashboard")


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Admin-only view for creating users within the company."""

    model = CustomUser
    form_class = UserCreateForm
    template_name = "user_create.html"

    def form_valid(self, form):
        """Assigns the company to the new user and saves it."""
        company = get_current_company()
        if not company:
            messages.error(self.request, "No active company found.")
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.company = company
        user.set_password(form.cleaned_data["password"])  # Ensure password is hashed
        user.save()

        messages.success(self.request, "User created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "company_settings:user_management",
            kwargs={"name": self.request.user.company.name},
        )


class UserEditView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Allows admins to edit user details."""

    model = CustomUser
    form_class = UserEditForm
    template_name = "user_edit.html"

    def form_valid(self, form):
        messages.success(self.request, "User information updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error updating the user information."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "company_settings:user_management",
            kwargs={"name": self.request.user.company.name},
        )
