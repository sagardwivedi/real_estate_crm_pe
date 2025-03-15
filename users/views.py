import json

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, UpdateView

from leads.views import GroupRequiredMixin
from tenants.middleware import get_current_company
from users.forms import (
    AdminSignupForm,
    CompanySignupForm,
    CustomLoginForm,
    UserCreateForm,
    UserEditForm,
)
from users.models import CustomUser
from users.service import UserRedirectionService, UserSignupService


class SignupView(TemplateView):
    template_name = "signup.html"

    def post(self, request):
        company_form = CompanySignupForm(request.POST)
        admin_form = AdminSignupForm(request.POST)

        if company_form.is_valid() and admin_form.is_valid():
            company = UserSignupService.create_company_admin(
                company_form, admin_form, request
            )
            messages.success(request, "Company and admin account created successfully!")
            return redirect(reverse_lazy("dashboard", kwargs={"name": company.name}))

        messages.error(request, "Please correct the errors below.")
        return self.render_to_response(
            self.get_context_data(company_form=company_form, admin_form=admin_form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault(
            "company_form", kwargs.get("company_form", CompanySignupForm())
        )
        context.setdefault("admin_form", kwargs.get("admin_form", AdminSignupForm()))
        return context


class CustomLoginView(LoginView):
    """Custom login view with role-based redirection."""

    template_name = "login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return UserRedirectionService.get_redirect_url(self.request.user)


class UserCreateView(GroupRequiredMixin, CreateView):
    """Admin-only view for creating users within the company."""

    model = CustomUser
    form_class = UserCreateForm
    template_name = "user_create.html"

    def form_valid(self, form):
        company = get_current_company()
        if not company:
            messages.error(self.request, "No active company found.")
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.company = company
        user.save()

        messages.success(self.request, "User created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "company_settings:user_management",
            kwargs={"name": self.request.user.company.name},
        )


class UserEditView(GroupRequiredMixin, UpdateView):
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


class GetUserThemeView(View):
    """Fetches the user's theme preference from the database."""

    def get(self, request, *args, **kwargs):
        return JsonResponse({"theme": request.user.theme_preference})


@method_decorator(csrf_exempt, name="dispatch")
class SetUserThemeView(View):
    """Updates the user's theme preference and syncs with LocalStorage."""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            new_theme = data.get("theme")

            if new_theme not in ["light", "dark"]:
                return JsonResponse({"error": "Invalid theme"}, status=400)

            # Save in database
            request.user.theme_preference = new_theme
            request.user.save()

            return JsonResponse(
                {"message": "Theme updated successfully", "theme": new_theme}
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
