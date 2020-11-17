import datetime

from api.models import Company, User
from contracts.models import Contract, Offer
from rest_framework import serializers


class ContractSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    months = serializers.IntegerField(write_only=True, min_value=1, max_value=12)
    is_end = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = ("end_date", "customer", "personal_coefficient")

    def get_is_end(self, contract: Contract) -> bool:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        return now > contract.end_date

    def create(self, validated_data):
        validated_data.pop("months", None)
        return super().create(validated_data)


class OfferSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    months = serializers.IntegerField(write_only=True, min_value=1, max_value=12)

    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ("status",)
