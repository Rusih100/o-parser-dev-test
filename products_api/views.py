# views.py
from rest_framework.request import Request
from rest_framework.views import APIView


class StartParsingView(APIView):
    def post(self, request: Request):
        return {}
