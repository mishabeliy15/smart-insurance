from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


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


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
