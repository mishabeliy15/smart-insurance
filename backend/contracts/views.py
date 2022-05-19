import datetime

from rest_framework.response import Response

from contracts.filters import ContractFilterBackend
from contracts.models import Contract, Offer
from contracts.serializers import ContractSerializer, OfferSerializer, ContractDetailSerializer
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet


class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all().order_by("-created")
    serializer_class = ContractSerializer
    filter_backends = (ContractFilterBackend, DjangoFilterBackend, SearchFilter)
    permission_classes = (DRYPermissions,)
    filterset_fields = (
        "id",
        "company",
        "customer",
        "end_date",
        "personal_coefficient",
        "created",
        "updated",
    )
    search_fields = (
        "id",
        "company__name",
        "customer__username",
    )

    def get_serializer_class(self):
        if self.action == "my_detail":
            return ContractDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        delta = datetime.timedelta(days=serializer.validated_data["months"] * 30)
        end_date = datetime.datetime.now(tz=datetime.timezone.utc) + delta
        serializer.save(customer=self.request.user, end_date=end_date)

    @action(detail=False, methods=("GET",))
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=("GET",))
    def my_detail(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all().order_by("-created")
    serializer_class = OfferSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = (DRYPermissions,)
    filterset_fields = (
        "id",
        "status",
        "company",
        "customer",
        "months",
        "personal_coefficient",
        "created",
        "updated",
    )
    search_fields = (
        "id",
        "company__name",
        "customer__username",
    )

    @action(detail=False, methods=("GET",))
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["company"].owner != self.request.user:
            raise APIException(code=400, detail=_("User must be owner the company."))
        serializer.save()

    @action(detail=True, methods=("POST",))
    def accept(self, request, pk=None):
        offer = self.get_object()
        contract = offer.accept()
        data = ContractSerializer(contract).data
        return Response(data=data)

    @action(detail=True, methods=("POST",))
    def deny(self, request, pk=None):
        offer = self.get_object()
        offer.status = offer.status = offer.DENIED
        data = OfferSerializer(offer).data
        return Response(data=data)
