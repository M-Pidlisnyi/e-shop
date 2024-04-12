from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from decimal import Decimal

from .models import Product, Order, Customer
from .forms import CreateOrderForm

# Create your views here.
class IndexView(ListView):
    model = Product
    template_name = "index.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


class CreateOrderView(LoginRequiredMixin, FormView):
    model = Order
    template_name = "create_order.html"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        form = CreateOrderForm()
        return render(request, self.template_name, {"form": form})
    def post(self, request, *args, **kwargs):
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            customer = Customer.objects.get(user=request.user)



            product  = form.cleaned_data["product"]
            amount   = form.cleaned_data["amount"]

            Order.objects.create(
                product=product,
                customer=customer,
                amount=amount,
                price_with_discount= (product.price - (product.price * customer.discount_value/100))*amount

            )
            customer.update_discount()
        return HttpResponseRedirect(reverse("order-list"))





class OrderListView(ListView):
    model = Order
    template_name = "order_list.html"

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if not self.request.user.is_superuser:
            return super().get(request, *args, **kwargs)

        username = request.GET.get("customer", "misha")

        customer = Customer.objects.select_related("user").get(user__username=username)

        context = self.get_context_data()
        context["desired_customer_order_history"] = Order.objects.filter(customer=customer).prefetch_related("customer", "product")
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_customer_order_history"] = Order.objects.filter(customer=self.request.user.customer).prefetch_related("customer", "product")
        if self.request.user.is_superuser:
            context["customers_list"] = Customer.objects.select_related("user").exclude(order_history=None)

        return context