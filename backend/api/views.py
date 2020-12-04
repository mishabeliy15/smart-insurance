from api.filters import CompanyFilterBackend
from api.models import Company, User
from api.serializers import (
    CompanySerializer,
    DriverCompanySerializer,
    PotentialClientSerializer,
)
from django.contrib import messages
from django.core import management
from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
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
    filter_backends = (CompanyFilterBackend, DjangoFilterBackend, SearchFilter)
    permission_classes = (DRYPermissions,)
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
    search_fields = (
        "id",
        "name",
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=("GET",))
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=("GET",))
    def personal_price(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DriverCompanySerializer(
            queryset, many=True, user=self.request.user
        )
        serializer_data = sorted(serializer.data, key=lambda k: k["own_price"])
        return Response(serializer_data)

    @action(detail=True, methods=("GET",))
    def potential_clients(self, request, *args, **kwargs):
        company = self.get_object()
        drivers = User.objects.filter(user_type=User.DRIVER)
        serializer = PotentialClientSerializer(drivers, many=True, company=company)
        serializer_data = sorted(serializer.data, key=lambda k: k["own_price"])
        return Response(serializer_data)


class BackupView(APIView):
    def get(self, request, format=None):
        management.call_command("dbbackup", "--noinput")
        messages.success(request, "Backup hash been successful created.")
        return HttpResponseRedirect(redirect_to="/admin/")


class RestoreView(APIView):
    def get(self, request, format=None):
        management.call_command("dbrestore", "--noinput")
        messages.success(request, "Database hash been successful restored.")
        return HttpResponseRedirect(redirect_to="/admin/")
