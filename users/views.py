from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from leads.views import AdminRequiredMixin
from users.forms import AdminSignupForm, CompanySignupForm, CustomLoginForm
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
        return self.render_to_response(
            self.get_context_data(company_form=company_form, admin_form=admin_form)
        )

    def form_valid(self, company_form, admin_form):
        # Save company and generate a slug
        company = company_form.save()
        # Save the admin user and assign the company
        admin_user = admin_form.save(company=company)

        # Log in the user
        login(self.request, admin_user)

        # Redirect to the company-specific dashboard
        return redirect(
            reverse_lazy("dashboard", kwargs={"company_slug": company.slug})
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault(
            "company_form", kwargs.get("company_form", CompanySignupForm())
        )
        context.setdefault("admin_form", kwargs.get("admin_form", AdminSignupForm()))
        return context


class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirect to the logged-in user's company dashboard
        user = self.request.user
        if user.is_authenticated and user.company:
            return reverse_lazy("dashboard", kwargs={"name": user.company.name})
        return reverse_lazy("dashboard")


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("users:user_list")

    def form_valid(self, form):
        # Save the form and show a success message
        messages.success(self.request, "User created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Show error message if the form is invalid
        messages.error(self.request, "There was an error creating the user.")
        return super().form_invalid(form)


class UserEditView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserChangeForm  # Django's built-in UserChangeForm for editing users
    template_name = "user_edit.html"
    success_url = reverse_lazy("users:user_list")

    def get_object(self):
        # This is used to fetch the user based on the URL, allowing you to edit the selected user.
        return self.get_queryset().get(id=self.kwargs["pk"])

    def form_valid(self, form):
        messages.success(self.request, "User information updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error updating the user information."
        )
        return super().form_invalid(form)
