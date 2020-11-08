import hashlib

from django.contrib.auth.models import AbstractUser
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
        choices=USER_TYPE_CHOICES, default=DRIVER, verbose_name=_("User type"),
    )

    def __str__(self) -> str:
        return self.username


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
    base_price = models.FloatField(verbose_name=_("Base price"))
    min_price = models.FloatField(verbose_name=_("Min price"))
    max_price = models.FloatField(verbose_name=_("Max price"))

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

    def has_object_write_permission(self, request) -> bool:
        return request.user.is_superuser or request.user == self.owner
