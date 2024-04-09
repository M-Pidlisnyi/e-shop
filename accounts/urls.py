from  django.urls import path, include
from django.views.generic import TemplateView
from .views import RegistrationView


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", RegistrationView.as_view(), name="register"),
]