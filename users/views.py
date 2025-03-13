from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import TemplateView

from users.forms import AdminSignupForm, CompanySignupForm, CustomLoginForm


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
        company = company_form.save(commit=False)
        company.slug = slugify(company.name)  # Create a URL-friendly slug
        company.save()

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
