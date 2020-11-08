from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.serializers import ModelSerializer
from sensors.models import Sensor


class SensorSerializer(ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Sensor
        exclude = ("owner",)
