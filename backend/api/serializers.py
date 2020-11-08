from rest_framework.serializers import ModelSerializer

from api.models import User


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "user_type")
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "user_type": {"required": True, "allow_blank": False},
        }
