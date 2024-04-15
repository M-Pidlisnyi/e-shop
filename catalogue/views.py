from django.db.models import Count, Avg
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from decimal import Decimal

from .models import Product, Order, Customer, Category
from .forms import CreateOrderForm

# Create your views here.
class IndexView(ListView):
    model = Product
    template_name = "index.html"

    def get_queryset(self):
        return Product.objects.annotate(order_num=Count('order')).filter(order_num__gt=0).order_by('-order_num')


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"]  = self.object.product_set.all()
        context["avg_price"] = self.object.product_set.aggregate(Avg('price'))["price__avg"]
        return context


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
        current_customer_order_history = Order.objects.filter(customer=self.request.user.customer).prefetch_related("customer", "product")
        # context["current_customer_order_history"]  = current_customer_order_history

        order_history_with_additional_details = []
        for order in current_customer_order_history:
            undiscounted_price = order.product.price
            discounted_price = order.price_with_discount/order.amount
            difference = undiscounted_price - discounted_price
            order_history_with_additional_details.append((order, difference))

        context["order_history"] = order_history_with_additional_details

        context["orders_num"] = current_customer_order_history.count()
        #print(current_customer_order_history.explain())
        if self.request.user.is_superuser:
            customers_list = Customer.objects.prefetch_related("user").exclude(order_history=None)
            context["customers_list"] = customers_list
            print(customers_list.explain())

        return context