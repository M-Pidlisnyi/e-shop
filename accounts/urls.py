from  django.urls import path, include
from django.views.generic import TemplateView
from .views import RegistrationView, ProfileView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", RegistrationView.as_view(), name="register"),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile")
]