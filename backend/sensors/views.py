import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_gis.filters import (
    DistanceToPointFilter,
    DistanceToPointOrderingFilter,
)
from sensors.clients import MyMappiRoadAPIClient
from sensors.filters import SensorFilterBackend, SensorRecordFilterBackend
from sensors.models import HeadRotateRecord, Sensor, SpeedRecord
from sensors.serializers import (
    CreateHeadRotateRecordSerializer,
    CreateSensorSerializer,
    DefaultSensorSerializer,
    DetailHeadRotateRecordSerializer,
    SpeedRecordSerializer,
)


class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (SensorFilterBackend, DjangoFilterBackend, SearchFilter)
    filterset_fields = (
        "uuid",
        "sensor_type",
        "owner",
        "created",
        "updated",
    )
    search_fields = ("uuid", "owner")

    serializer_class = {
        "create": CreateSensorSerializer,
        "default": DefaultSensorSerializer,
    }

    def get_serializer_class(self):
        cls = self.serializer_class.get(self.action, self.serializer_class["default"])
        return cls

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=("GET",))
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SpeedRecordViewSet(ModelViewSet):
    queryset = SpeedRecord.objects.select_related("sensor").all()
    serializer_class = SpeedRecordSerializer
    filter_backends = (
        SensorRecordFilterBackend,
        DistanceToPointFilter,
        DistanceToPointOrderingFilter,
        DjangoFilterBackend,
        SearchFilter,
    )
    distance_ordering_filter_field = "location"
    distance_filter_field = "location"
    filterset_fields = (
        "id",
        "speed",
        "sensor__owner",
        "over_speed",
        "created",
        "updated",
    )
    search_fields = ("id", "sensor__owner")

    api_client = MyMappiRoadAPIClient()

    def perform_create(self, serializer):
        if serializer.is_valid():
            p = serializer.validated_data["location"]
            max_speed = self.api_client.get_speed_limit(p.y, p.x)
            over_speed = serializer.validated_data["speed"] / max_speed
            serializer.save(over_speed=over_speed)


class HeadRotateRecordViewSet(ModelViewSet):
    queryset = HeadRotateRecord.objects.select_related("sensor").all()
    filter_backends = (
        SensorRecordFilterBackend,
        DistanceToPointFilter,
        DistanceToPointOrderingFilter,
        DjangoFilterBackend,
        SearchFilter,
    )
    distance_ordering_filter_field = "speed__location"
    distance_filter_field = "speed__location"
    filterset_fields = (
        "id",
        "angle",
        "sensor__owner",
        "created",
        "updated",
    )
    search_fields = ("id", "sensor__owner")

    serializer_class = {
        "create": CreateHeadRotateRecordSerializer,
        "default": DetailHeadRotateRecordSerializer,
    }

    def get_serializer_class(self):
        cls = self.serializer_class.get(self.action, self.serializer_class["default"])
        return cls

    def perform_create(self, serializer):
        now_date = datetime.datetime.now(datetime.timezone.utc)
        delta = datetime.timedelta(seconds=3)
        if serializer.is_valid():
            user = serializer.validated_data["sensor"].owner
            speed = SpeedRecord.objects.near_date(user, now_date, delta)
            serializer.save(speed=speed)
