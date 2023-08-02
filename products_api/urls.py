from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("products", views.ProductList.as_view()),
    path("products/<int:pk>", views.ProductDetail.as_view()),
    path("", include(router.urls)),
]

urlpatterns += router.urls
