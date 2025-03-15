from django.contrib.auth import login
from django.contrib.auth.models import AbstractUser, Group
from django.urls import reverse_lazy


class UserSignupService:
    """Handles user registration and assignment to a company."""

    @staticmethod
    def create_company_admin(company_form, admin_form, request):
        company = company_form.save()
        admin_user = admin_form.save(commit=False)
        admin_user.company = company
        admin_user.save()

        UserSignupService.assign_group(admin_user, "Company Admin")

        login(request, admin_user)
        return company

    @staticmethod
    def assign_group(user: AbstractUser, group_name):
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)


class UserRedirectionService:
    """Handles role-based dashboard redirection."""

    GROUP_REDIRECTS = {
        "Company Admin": "dashboard",
        "Sales Manager": "sales_manager_dashboard",
        "Agent": "agent_dashboard",
    }

    @staticmethod
    def get_redirect_url(user: AbstractUser) -> str:
        """Return the correct dashboard URL based on the user role."""
        dashboard_route = UserRedirectionService.get_dashboard_route(user)
        return reverse_lazy(dashboard_route, kwargs={"name": user.company.name})

    @staticmethod
    def get_dashboard_route(user: AbstractUser) -> str:
        """Determine the appropriate dashboard route for the user."""
        user_groups = set(user.groups.values_list("name", flat=True))

        for group_name, route in UserRedirectionService.GROUP_REDIRECTS.items():
            if group_name in user_groups:
                return route

        return "users:login"  # Default if no matching role
