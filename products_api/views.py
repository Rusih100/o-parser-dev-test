# views.py
from rest_framework import generics
from products_api.models import Product
from products_api.serializers import ProductSerializers


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
