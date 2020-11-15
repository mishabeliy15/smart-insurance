from api.models import Company, User
from django.utils.translation import gettext as _
from djoser.serializers import UserCreateSerializer
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from sensors.models import SpeedRecord


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            *UserCreateSerializer.Meta.fields,
            "first_name",
            "last_name",
            "user_type",
        )
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "user_type": {"required": True},
        }


class CurrentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class CompanySerializer(ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Company
        exclude = ("owner",)

    def validate(self, data):
        if data["min_price"] > data["base_price"]:
            raise ValidationError(_("Min price must be <= base price."))
        if data["max_price"] < data["base_price"]:
            raise ValidationError(_("Max price must be >= base price."))
        return data


class DriverCompanySerializer(ModelSerializer):
    own_speed_discount = SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.avg_over_speed = SpeedRecord.get_avg_user_over_speed(self.user)
        super(DriverCompanySerializer, self).__init__(*args, **kwargs)

    @staticmethod
    def _own_price(data):
        price = data["base_price"] - data["own_speed_discount"]
        price = max(price, data["min_price"])
        price = min(price, data["max_price"])
        price = round(price, 2)
        return price

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["own_price"] = self._own_price(data)
        return data

    def get_own_speed_discount(self, obj: Company):
        discount = obj.base_price - self.avg_over_speed * obj.base_price
        if discount > 0:
            discount = min(discount, obj.max_speed_discount)
        elif discount < 0:
            discount = -min(-discount, obj.max_speed_penalty)
        return round(discount, 2)
