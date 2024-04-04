from django.urls import  path
from .views import IndexView, ProductDetailView
urlpatterns = [
    path("", IndexView.as_view(template_name="base.html"), name="home"),
    path("featured/", IndexView.as_view(), name="home"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product-detail")
]