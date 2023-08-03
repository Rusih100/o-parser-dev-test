from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products_api.models import Product
from products_api.paginator import Paginator
from products_api.serializers import ParseViewSerializer, ProductSerializer


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsApiView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            paginator = Paginator()
            queryset = Product.objects.all()
            result_page = paginator.paginate_queryset(
                queryset=queryset, request=request
            )
            serializer = ProductSerializer(result_page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except APIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            serializer = ParseViewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product_count = serializer.validated_data.get("product_count", 10)
            return Response(
                {
                    "detail": f"A request for parsing {product_count} records has been created"
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except APIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
