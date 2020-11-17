import datetime

from api.models import Company, User
from commons.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from dry_rest_permissions.generics import authenticated_users
from rest_framework.exceptions import APIException


class Contract(BaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name=_("Company"), editable=False
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Customer"), editable=False
    )
    end_date = models.DateTimeField(verbose_name=_("End date"))
    personal_coefficient = models.FloatField(
        validators=(MinValueValidator(0.01), MaxValueValidator(100)),
        default=1,
        verbose_name=_("Personal price coefficient"),
    )

    @staticmethod
    @authenticated_users
    def has_read_permission(request) -> bool:
        return request.user.is_superuser

    @authenticated_users
    def has_object_read_permission(self, request) -> bool:
        return request.user.is_superuser or request.user.pk in (
            self.company.owner.pk,
            self.customer.pk,
        )

    @staticmethod
    @authenticated_users
    def has_create_permission(request) -> bool:
        return (
            request.user.is_superuser or request.user.user_type == request.user.DRIVER
        )

    @authenticated_users
    def has_object_write_permission(self, request) -> bool:
        return request.user.is_superuser or request.user == self.customer

    @staticmethod
    @authenticated_users
    def has_my_permission(request) -> bool:
        return True


class Offer(BaseModel):
    PENDING = 1
    ACCEPTED = 2
    DENIED = 3
    CANCELED = 4

    STATUSES = (
        (PENDING, _("PENDING")),
        (ACCEPTED, _("ACCEPTED")),
        (DENIED, _("DENIED")),
        (CANCELED, _("CANCELED")),
    )

    status = models.PositiveSmallIntegerField(
        choices=STATUSES, default=PENDING, verbose_name=_("Status"),
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name=_("Company"), editable=False
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Customer"), editable=False
    )
    months = models.IntegerField(
        verbose_name=_("Months"),
        validators=(MinValueValidator(1), MaxValueValidator(12)),
    )

    personal_coefficient = models.FloatField(
        validators=(MinValueValidator(0.01), MaxValueValidator(100)),
        default=1,
        verbose_name=_("Personal price coefficient"),
    )

    def accept(self) -> Contract:
        if self.status != self.PENDING:
            raise APIException(code=400, detail=_('Status must be "Pending"'))

        delta = datetime.timedelta(days=self.months * 30)
        end_date = datetime.datetime.now(tz=datetime.timezone.utc) + delta
        contract = Contract.objects.create(
            company=self.company,
            customer=self.customer,
            personal_coefficient=self.personal_coefficient,
            end_date=end_date,
        )
        self.status = self.ACCEPTED
        self.save(update_fields=("status",))
        return contract

    @staticmethod
    @authenticated_users
    def has_read_permission(request) -> bool:
        return request.user.is_superuser

    @authenticated_users
    def has_object_read_permission(self, request) -> bool:
        return request.user.is_superuser or request.user.pk in (
            self.company.owner.pk,
            self.customer.pk,
        )

    @staticmethod
    @authenticated_users
    def has_create_permission(request) -> bool:
        return (
            request.user.is_superuser or request.user.user_type == request.user.BUSINESS
        )

    @authenticated_users
    def has_object_write_permission(self, request) -> bool:
        return request.user.is_superuser or request.user == self.company.owner

    @staticmethod
    @authenticated_users
    def has_my_permission(request) -> bool:
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request) -> bool:
        return True

    @authenticated_users
    def has_object_accept_permission(self, request) -> bool:
        return request.user.is_superuser or request.user == self.customer
