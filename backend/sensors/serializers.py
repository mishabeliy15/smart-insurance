from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_gis.serializers import GeoModelSerializer
from sensors.models import Sensor, SpeedRecord


class CreateSensorSerializer(serializers.ModelSerializer):
    sensor_type = serializers.ChoiceField(Sensor.SENSOR_TYPES)
    uuid = serializers.UUIDField(
        validators=(UniqueValidator(queryset=Sensor.objects.all()),)
    )

    class Meta:
        model = Sensor
        fields = ("uuid", "sensor_type")


class DefaultSensorSerializer(CreateSensorSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"


class SpeedRecordSerializer(GeoModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())
    speed = serializers.FloatField(min_value=0, max_value=400)
    location = PointField()

    class Meta:
        model = SpeedRecord
        fields = "__all__"
        read_only_fields = ("over_speed",)
