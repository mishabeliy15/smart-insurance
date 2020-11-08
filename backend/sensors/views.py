from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from sensors.filters import SensorFilterBackend
from sensors.models import Sensor
from sensors.serializers import SensorSerializer


class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=("GET",))
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
