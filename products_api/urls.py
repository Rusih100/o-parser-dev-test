from django.urls import path

from . import views

urlpatterns = [
    path("products", views.ProductsApiView.as_view(), name="products"),
    path("products/<int:pk>", views.ProductDetail.as_view(), name="detail_product"),
]
