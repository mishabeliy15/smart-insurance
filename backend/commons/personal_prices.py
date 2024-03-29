import datetime
from collections import namedtuple

from api.models import Company, User
from insurance.settings import HEAD_ANGLE_RECORD_MAX_INTERVAL
from sensors.models import HeadRotateRecord, SpeedRecord


class PersonalPrices:
    UserPrice = namedtuple(
        "UserPrice", ("price", "speed_discount", "head_rotate_discount")
    )

    def __init__(self, user: User):
        self.user = user
        self.avg_over_speed = SpeedRecord.get_avg_user_over_speed(self.user)
        self.head_records = HeadRotateRecord.get_user_records(self.user)

    def get_detail_price(self, company: Company) -> UserPrice:
        speed_discount = self.get_own_speed_discount(company)
        head_rotate_discount = self.get_own_head_rotate_discount(company)
        price = self.get_price(company, speed_discount, head_rotate_discount)
        detail_price = self.UserPrice(price, speed_discount, head_rotate_discount)
        return detail_price

    def get_price(
        self, company: Company, speed_discount: float, head_rotate_discount: float
    ) -> float:
        price = company.base_price - speed_discount - head_rotate_discount
        price = self._adjust_price(company, price)
        return price

    @staticmethod
    def _adjust_price(company: Company, price: float) -> float:
        price = max(price, company.min_price)
        price = min(price, company.max_price)
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

    @staticmethod
    def _adjust_discount(
        max_discount: float, max_penalty: float, discount: float
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

    def _get_ratio_head(self, obj: Company) -> float:
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
