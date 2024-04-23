from django.urls import  path
from django.views.generic import RedirectView
from .views import IndexView, ProductDetailView, CreateOrderView, OrderListView, CategoryDetailView, CategoryListView, \
    ProductListView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="home")),
    path("featured/", IndexView.as_view(), name="home"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("products/list", ProductListView.as_view(), name="product-list"),
    path("new/", CreateOrderView.as_view(), name="create-order"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("category/<int:pk>", CategoryDetailView.as_view(), name="category-detail"),
    path("category/list/", CategoryListView.as_view(), name="category-list")
]