import hashlib

from commons.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from dry_rest_permissions.generics import authenticated_users


class User(AbstractUser):
    DRIVER = 1
    BUSINESS = 2

    USER_TYPE_CHOICES = (
        (DRIVER, _("DRIVER")),
        (BUSINESS, _("BUSINESS")),
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=DRIVER,
        editable=False,
        verbose_name=_("User type"),
    )

    def __str__(self) -> str:
        return self.username


def company_directory_path(instance: "Company", filename: str) -> str:
    company_dir = f"user_{instance.owner.id}/company/{instance.md5_name}/{filename}"
    return company_dir


class Company(BaseModel):
    name = models.CharField(
        max_length=64, unique=True, db_index=True, verbose_name=_("Name")
    )
    owner = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name=_("Owner"))
    logo = models.ImageField(
        upload_to=company_directory_path, verbose_name=_("Company logo")
    )

    base_price = models.FloatField(
        validators=(MinValueValidator(0),), verbose_name=_("Base price")
    )
    min_price = models.FloatField(
        validators=(MinValueValidator(0),), verbose_name=_("Min price")
    )
    max_price = models.FloatField(
        validators=(MinValueValidator(0),), verbose_name=_("Max price")
    )

    percent_over_speeding = models.FloatField(
        validators=(MinValueValidator(1), MaxValueValidator(100)),
        verbose_name=_("Percent allowed over speeding"),
    )

    min_speed_commit_rotate_head = models.FloatField(
        validators=(MinValueValidator(0), MaxValueValidator(200)),
        verbose_name=_("Minimum speed to commit rotate head"),
    )

    min_angle_commit_rotate_head = models.SmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(90)),
        verbose_name=_("Minimum angle to commit rotate head"),
        default=40,
    )

    percent_head_rotate_for_hour = models.FloatField(
        validators=(MinValueValidator(1), MaxValueValidator(100)),
        verbose_name=_("Percent head rotation for hour"),
    )

    max_speed_discount = models.FloatField(
        validators=(MinValueValidator(0),), verbose_name=_("Max speed discount"),
    )
    max_speed_penalty = models.FloatField(
        validators=(MinValueValidator(0),), verbose_name=_("Max speed penalty"),
    )

    max_rotate_head_discount = models.FloatField(
        validators=(MinValueValidator(0),), verbose_name=_("Max rotate head discount"),
    )
    max_rotate_head_penalty = models.FloatField(
        validators=(MinValueValidator(0),), verbose_name=_("Max rotate head penalty"),
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=models.Q(min_price__lte=models.F("base_price")),
                name=_("Min price must be <= base price."),
            ),
            models.CheckConstraint(
                check=models.Q(max_price__gte=models.F("base_price")),
                name=_("Max price must be >= base price."),
            ),
        )

    @property
    def md5_name(self) -> str:
        byte_str = self.name.encode("utf-8")
        md5 = hashlib.md5(byte_str).hexdigest()
        return md5

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def has_read_permission(request) -> bool:
        return True

    def has_object_read_permission(self, request) -> bool:
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request) -> bool:
        return (
            request.user.is_superuser or request.user.user_type == request.user.BUSINESS
        )

    @staticmethod
    @authenticated_users
    def has_my_permission(request) -> bool:
        return request.user.user_type == request.user.DRIVER

    def has_object_write_permission(self, request) -> bool:
        return request.user.is_superuser or request.user == self.owner

    @staticmethod
    @authenticated_users
    def has_personal_price_permission(request) -> bool:
        return request.user.user_type == request.user.DRIVER
