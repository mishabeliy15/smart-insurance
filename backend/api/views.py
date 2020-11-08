from api.filters import CompanyFilterBackend
from api.models import Company, User
from api.serializers import CompanySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
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
    filter_backends = (CompanyFilterBackend, DjangoFilterBackend, SearchFilter)
    filterset_fields = (
        "id",
        "name",
        "owner",
        "base_price",
        "min_price",
        "max_price",
        "percent_over_speeding",
        "min_speed_commit_rotate_head",
        "percent_head_rotate_for_hour",
        "max_speed_discount",
        "max_speed_penalty",
        "max_rotate_head_discount",
        "max_rotate_head_penalty",
        "created",
        "updated",
    )
    search_fields = ("id", "name",)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=("GET",), permission_classes=(IsAuthenticated,))
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
