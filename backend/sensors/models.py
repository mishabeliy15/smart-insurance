import datetime

from api.models import User
from commons.models import BaseModel
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _
from dry_rest_permissions.generics import authenticated_users

from insurance.settings import SPEED_RECORD_MAX_INTERVAL
from sensors.managers import NearDateManger


class Sensor(BaseModel):
    SPEED = 1
    HEAD_ANGLE = 2

    SENSOR_TYPES = (
        (SPEED, _("SPEED"),),
        (HEAD_ANGLE, _("HEAD_ANGLE"),),
    )

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        unique=True,
        primary_key=True,
        editable=False,
        db_index=True,
    )
    sensor_type = models.PositiveSmallIntegerField(
        choices=SENSOR_TYPES, editable=False, verbose_name=_("Sensor type"),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Owner"),
        editable=False,
        db_index=True,
    )

    @staticmethod
    def has_read_permission(request) -> bool:
        return True

    def has_object_read_permission(self, request) -> bool:
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request) -> bool:
        return (
            request.user.is_superuser or request.user.user_type == request.user.DRIVER
        )

    def has_object_write_permission(self, request) -> bool:
        return request.user.is_superuser or request.user == self.owner


class BaseSensorRecord(BaseModel):
    sensor = models.ForeignKey(
        Sensor,
        verbose_name=_("Sensor"),
        on_delete=models.CASCADE,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True

    @staticmethod
    @authenticated_users
    def has_read_permission(request) -> bool:
        return True

    @authenticated_users
    def has_object_read_permission(self, request) -> bool:
        return request.user.is_superuser or self.sensor.owner == request.user

    @staticmethod
    def has_create_permission(request) -> bool:
        return True

    @authenticated_users
    def has_object_destroy_permission(self, request) -> bool:
        return request.user.is_superuser

    @authenticated_users
    def has_object_update_permission(self, request) -> bool:
        return False


class SpeedRecord(BaseSensorRecord):
    speed = models.FloatField(
        verbose_name=_("Speed"),
        validators=(MinValueValidator(0), MaxValueValidator(400),),
        editable=False,
    )
    over_speed = models.FloatField(
        validators=(MinValueValidator(0),), verbose_name=_("Over speed")
    )
    location = models.PointField(
        geography=True, editable=False, verbose_name=_("Location")
    )

    objects = NearDateManger()

    @classmethod
    def get_avg_user_over_speed(cls, user) -> float:
        speed_records = list(
            cls.objects.filter(sensor__owner=user)
            .order_by("created")
            .values("created", "over_speed", "speed")
        )
        total_seconds = total_over_speed = 0
        prev_record = {
            "created": datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
        }
        for record in speed_records:
            interval = (record["created"] - prev_record["created"]).total_seconds()
            if (
                interval > SPEED_RECORD_MAX_INTERVAL
                or prev_record["speed"] == record["speed"] == 0
            ):
                prev_record = record
                continue
            avg_over = (prev_record["over_speed"] + record["over_speed"]) / 2
            total_seconds += interval
            total_over_speed += avg_over * interval
        avg_over_speed = total_over_speed / total_seconds
        return avg_over_speed


class HeadRotateRecord(BaseSensorRecord):
    speed = models.ForeignKey(
        SpeedRecord,
        on_delete=models.CASCADE,
        editable=False,
        db_index=True,
        verbose_name=_("Speed"),
    )
    angle = models.SmallIntegerField(
        verbose_name=_("Rotate head angle"),
        validators=(MinValueValidator(-360), MaxValueValidator(360),),
        db_index=True,
        editable=False,
    )
