from rest_framework.views import APIView
from rest_framework.response import Response
import json

# from .serializer import NameSerializer
# from .models import Name

class NameView(APIView):
    def post(self, request):
        return Response(json.loads(request.body))