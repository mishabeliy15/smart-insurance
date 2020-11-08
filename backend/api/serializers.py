from djoser.serializers import UserCreateSerializer


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = [*UserCreateSerializer.Meta.fields, "user_type"]
        extra_kwargs = {
            "user_type": {"required": True, "allow_blank": False},
        }
