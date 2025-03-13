from threading import local

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

_thread_locals = local()


def get_current_company():
    return getattr(_thread_locals, "company", None)


def set_current_company(company):
    _thread_locals.company = company


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if request.user.is_authenticated and hasattr(request.user, "company"):
            set_current_company(request.user.company.id)

    def process_response(self, request: HttpRequest, response: HttpResponse):
        _thread_locals.company = None
        return response
