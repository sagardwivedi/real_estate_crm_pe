from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, SignupView, UserCreateView, UserEditView

app_name = "users"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", UserEditView.as_view(), name="edit"),  # Edit user by pk
]
