from django.db.models import Count, Avg
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader


from decimal import Decimal

from .models import Product, Order, Customer, Category
from .forms import CreateOrderForm

# Create your views here.
class IndexView(ListView):
    model = Product
    template_name = "index.html"

    def get_queryset(self):
        return Product.objects.annotate(order_num=Count('order')).filter(order_num__gt=0).order_by('-order_num')

class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"

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

    def get(self, request, *args, **kwargs):

        if "form" in kwargs:# if we came here from post request of same view (i.e. there was error creating order)
            form = kwargs["form"]
        elif "product" in request.GET:# if we came here from "Buy" button in product list or details
            form = CreateOrderForm(initial={"product": request.GET["product"]})
        else:
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

        kwargs["form"] = form
        print(form.errors.as_data())
        return self.get(request, *args, **kwargs)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order_list.html"
    raise_exception = True
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
            # print(customers_list.explain())

        return context


class AddToBagView(RedirectView):
    """
        adds product to bag and immediately redirects to url where 'add to bag' button was pressed
    """
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id", None)
        if product_id:
            #prudct ids are saved in session like this: product_<id>: amount
            key = "product_" + product_id
            if key not in request.session:
                request.session[key] = 1
            else:
                request.session[key] += 1


        self.url = request.POST.get("from_url", reverse("home"))
        return HttpResponseRedirect(self.url)

class ShoppingBagView(TemplateView):
    template_name = 'shopping_bag.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        #filter out all other info from session, only product ids should be left
        #'product_' = 7 characters
        products_dict = {key[8:]:amount for key, amount in self.request.session.items() if key.startswith("product_")}
        # print(f"{products_dict=}")

        products = Product.objects.filter(id__in=products_dict.keys())
        context["bag_items"] = [(p,a) for p,a in zip(products, products_dict.values())]

        return context

    def post(self, request, *args, **kwargs):
        for product, amount in self.get_context_data()["bag_items"]:
            customer = request.user.customer
            Order.objects.create(
                product=product,
                amount=amount,
                customer=customer,
                price_with_discount= (product.price - (product.price * customer.discount_value/100))*amount)
            customer.update_discount()
        for key in list(request.session.keys()):
            if key.startswith("product_"):
                del request.session[key]
        return HttpResponseRedirect(reverse("home"))


class DeleteFromBagView(RedirectView):
    url = reverse_lazy('bag')
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id", None)
        if product_id:
            del request.session[product_id]
        return HttpResponseRedirect(self.url)



