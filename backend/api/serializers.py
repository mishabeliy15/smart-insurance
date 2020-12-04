from api.models import Company, User
from commons.personal_prices import PersonalPrices
from django.utils.translation import gettext as _
from djoser.serializers import UserCreateSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField
from rest_framework.serializers import ModelSerializer


class MyUserCreateSerializer(UserCreateSerializer):
    user_type = ChoiceField(User.USER_TYPE_CHOICES)

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
    class Meta:
        model = Company
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(DriverCompanySerializer, self).__init__(*args, **kwargs)
        self.price_client = PersonalPrices(self.user)

    def to_representation(self, company: Company):
        data = super().to_representation(company)
        detail_price = self.price_client.get_detail_price(company)
        data["own_speed_discount"] = detail_price.speed_discount
        data["own_head_rotate_discount"] = detail_price.head_rotate_discount
        data["own_price"] = detail_price.price
        return data


class PotentialClientSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "groups",
            "user_permissions",
        )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop("company")
        super(PotentialClientSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, driver: User):
        data = super().to_representation(driver)
        price_client = PersonalPrices(driver)
        detail_price = price_client.get_detail_price(self.company)
        data["own_speed_discount"] = detail_price.speed_discount
        data["own_head_rotate_discount"] = detail_price.head_rotate_discount
        data["own_price"] = detail_price.price
        return data
