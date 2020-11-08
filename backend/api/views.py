from api.models import User
from rest_framework.response import Response
from rest_framework.views import APIView


class MetaUserAPIView(APIView):
    def get(self, request, **kwargs):
        return Response(data=User.USER_TYPE_CHOICES)
