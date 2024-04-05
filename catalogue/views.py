from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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

            customer,new = Customer.objects.get_or_create(user=request.user, defaults={"discount_value": Decimal(0.99)})
            print(customer)
            if new:
                print("created new customer")



            Order.objects.create(
                product=form.cleaned_data["product"],
                customer=customer,
                amount=form.cleaned_data["amount"],
                price_with_discount= (form.cleaned_data["product"].price - (form.cleaned_data["product"].price * customer.discount_value/100))*form.cleaned_data["amount"]

            )



        return HttpResponseRedirect("/")



class OrderListView(ListView):
    model = Order
    template_name = "order_list.html"