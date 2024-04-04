from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.
class IndexView(ListView):
    model = Product
    template_name = "index.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


