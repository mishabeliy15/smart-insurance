from api.models import Company
from djoser.serializers import UserCreateSerializer
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.serializers import ModelSerializer


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = [*UserCreateSerializer.Meta.fields, "user_type"]
        extra_kwargs = {
            "user_type": {"required": True, "allow_blank": False},
        }


class CompanySerializer(ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Company
        # fields = "__all__"
        exclude = ("owner", )
