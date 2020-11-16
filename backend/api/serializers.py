import datetime

from api.models import Company, User
from django.utils.translation import gettext as _
from djoser.serializers import UserCreateSerializer
from dry_rest_permissions.generics import DRYPermissionsField
from insurance.settings import HEAD_ANGLE_RECORD_MAX_INTERVAL
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from sensors.models import HeadRotateRecord, SpeedRecord


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
    own_head_rotate_discount = SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(DriverCompanySerializer, self).__init__(*args, **kwargs)
        self.avg_over_speed = SpeedRecord.get_avg_user_over_speed(self.user)
        self.head_records = HeadRotateRecord.get_user_records(self.user)

    def to_representation(self, instance: Company):
        data = super().to_representation(instance)
        data["own_price"] = self._own_price(data)
        return data

    @staticmethod
    def _own_price(data) -> float:
        price = data["base_price"] - data["own_speed_discount"]
        price -= data["own_head_rotate_discount"]
        price = max(price, data["min_price"])
        price = min(price, data["max_price"])
        price = round(price, 2)
        return price

    def get_own_speed_discount(self, obj: Company) -> float:
        if self.avg_over_speed == 0:
            return 0.0
        percent = self.avg_over_speed - 1 - obj.percent_over_speeding / 100
        discount = obj.base_price * -percent
        discount = self._adjust_discount(
            obj.max_speed_discount, obj.max_speed_penalty, discount
        )
        return discount

    def _adjust_discount(
        self, max_discount: float, max_penalty: float, discount: float
    ) -> float:
        if discount > 0:
            discount = min(discount, max_discount)
        elif discount < 0:
            discount = -min(-discount, max_penalty)
        return round(discount, 2)

    def get_own_head_rotate_discount(self, obj: Company) -> float:
        ratio = self._get_ratio_head(obj)
        if ratio == 0:
            return 0.00

        ratio_discount = ratio - obj.percent_head_rotate_for_hour / 100
        discount = obj.base_price * -ratio_discount
        discount = self._adjust_discount(
            obj.max_rotate_head_discount, obj.max_rotate_head_penalty, discount
        )
        return discount

    def _get_ratio_head(self, obj: Company):
        total_drive_seconds = head_move_seconds = 0
        prev_record = {
            "created": datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
        }

        for head_record in self.head_records:
            interval = (head_record["created"] - prev_record["created"]).total_seconds()
            if interval > HEAD_ANGLE_RECORD_MAX_INTERVAL:
                prev_record = head_record
                continue

            if self._should_commit_head_record(head_record, obj):
                head_move_seconds += interval

            total_drive_seconds += interval
            prev_record = head_record

        if total_drive_seconds == 0:
            return 0

        ratio = head_move_seconds / total_drive_seconds

        return ratio

    @staticmethod
    def _should_commit_head_record(head_record: dict, company: Company) -> bool:
        return (
            head_record["angle"] >= company.min_angle_commit_rotate_head
            and head_record["speed__speed"] >= company.min_speed_commit_rotate_head
        )
