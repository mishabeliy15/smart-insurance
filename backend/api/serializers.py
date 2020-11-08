from api.models import Company
from djoser.serializers import UserCreateSerializer
from dry_rest_permissions.generics import DRYPermissionsField
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


class CompanySerializer(ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Company
        exclude = ("owner",)
