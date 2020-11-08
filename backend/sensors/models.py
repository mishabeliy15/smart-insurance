from django.core.validators import MinValueValidator, MaxValueValidator
from dry_rest_permissions.generics import authenticated_users

from api.models import User
from commons.models import BaseModel
from django.contrib.gis.db import models
from django.utils.translation import gettext as _


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


class SpeedRecord(BaseModel):
    sensor = models.ForeignKey(
        Sensor,
        verbose_name=_("Sensor"),
        on_delete=models.CASCADE,
        editable=False,
        db_index=True,
    )
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
