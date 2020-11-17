from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from django.utils.translation import gettext as _
from sensors.models import HeadRotateRecord, Sensor, SpeedRecord


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("uuid", "sensor_type", "owner", "created", "updated")
    list_filter = ("sensor_type", "owner", "created", "updated")
    fields = list_display
    readonly_fields = list_display


@admin.register(SpeedRecord)
class SpeedRecordAdmin(GeoModelAdmin):
    list_display = (
        "id",
        "speed",
        "over_speed",
        "location",
        "sensor",
        "created",
        "updated",
    )
    search_fields = ("id", "location")
    list_filter = ("sensor", "created", "updated")
    fields = list_display
    readonly_fields = list_display


@admin.register(HeadRotateRecord)
class HeadRotateRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "angle",
        "get_speed",
        "sensor",
        "created",
        "updated",
    )
    search_fields = ("id", "location")
    list_filter = ("sensor", "created", "updated")
    fields = list_display
    readonly_fields = list_display

    def get_speed(self, obj: HeadRotateRecord):
        return obj.speed.speed

    get_speed.short_description = _("Speed")
    get_speed.admin_order_field = "speed__speed"
