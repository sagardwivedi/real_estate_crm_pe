from threading import local

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

_thread_locals = local()


def get_current_company():
    """Returns the company associated with the current request."""
    return getattr(_thread_locals, "company", None)


def set_current_company(company):
    """Sets the current company in thread-local storage."""
    _thread_locals.company = company


class TenantMiddleware(MiddlewareMixin):
    """Middleware to enforce tenant-based access control."""

    def process_request(self, request: HttpRequest):
        """Checks if the user is authenticated and sets the company."""

        # If user is authenticated, set the company in thread-local storage
        if request.user.is_authenticated and hasattr(request.user, "company"):
            set_current_company(request.user.company)
            return  # Allow the request to proceed

        # Define allowed paths
        allowed_paths = {
            reverse("users:login"),
            reverse("users:signup"),
            reverse("landing"),
        }

        # Allow access to specific routes
        if (
            request.path.startswith(("/admin", "/__debug__/"))
            or request.path in allowed_paths
        ):
            return  # Allow access

        # Redirect unauthenticated users to the login page
        return redirect(reverse("users:login"))

    def process_response(self, request: HttpRequest, response: HttpResponse):
        """Clears the company reference after the request is processed."""
        _thread_locals.company = None
        return response
