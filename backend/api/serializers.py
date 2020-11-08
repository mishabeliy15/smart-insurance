from api.models import Company, User
from django.utils.translation import gettext as _
from djoser.serializers import UserCreateSerializer
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer


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
