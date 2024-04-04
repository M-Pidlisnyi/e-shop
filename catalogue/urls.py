from django.urls import  path
from django.views.generic import RedirectView
from .views import IndexView, ProductDetailView, CreateOrderView
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="home")),
    path("featured/", IndexView.as_view(), name="home"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("new/", CreateOrderView.as_view(), name="create-order")
]