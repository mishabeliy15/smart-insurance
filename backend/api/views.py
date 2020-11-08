from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.filters import CompanyFilterBackend
from api.models import Company, User
from api.serializers import CompanySerializer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class MetaUserAPIView(APIView):
    def get(self, request, **kwargs):
        return Response(data=User.USER_TYPE_CHOICES)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    parser_classes = (MultiPartParser, JSONParser)
    filter_backends = (CompanyFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=("GET",), permission_classes=(IsAuthenticated,))
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
