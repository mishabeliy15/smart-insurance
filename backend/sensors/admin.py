from django.contrib import admin
from sensors.models import Sensor


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("uuid", "sensor_type", "owner", "created", "updated")
    fields = list_display
    readonly_fields = list_display
