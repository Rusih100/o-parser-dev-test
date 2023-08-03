from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products_api.models import Product
from products_api.paginator import Paginator
from products_api.serializers import ProductSerializer
from products_api import tasks


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
            product_count = request.data.get("product_count", None)

            if product_count is None:
                product_count = 10
            elif 0 > product_count or product_count > 50:
                raise ValidationError("0 < product_count <= 50", code=status.HTTP_400_BAD_REQUEST)
            elif not isinstance(product_count, int):
                raise ValidationError("product_count is integer", code=status.HTTP_400_BAD_REQUEST)

            tasks.parsing_product_task.delay(product_count)
            return Response(
                {
                    "detail": f"A request for parsing {product_count} records has been created"
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except APIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
