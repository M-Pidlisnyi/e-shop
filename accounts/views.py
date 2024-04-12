from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User
from django.urls import  reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect

class RegistrationView(CreateView):
    model = User
    template_name = "registration/sign_up.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("order-list")

    def form_valid(self, form):
        print(form.cleaned_data)
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.success_url)

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    context_object_name = "customer"

    def get_object(self, queryset=None):
        return self.request.user.customer
