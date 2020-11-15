import datetime

from django.db.models import Manager
from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException


class NearDateManger(Manager):
    def bunch_near_date(
        self,
        user,
        timestamp: datetime.datetime,
        delta: datetime.timedelta = datetime.timedelta(seconds=5),
    ):
        min_date, max_date = timestamp - delta, timestamp + delta
        queryset = self.get_queryset()
        queryset = queryset.filter(
            created__gte=min_date, created__lte=max_date, sensor__owner=user
        )
        return queryset

    def near_date(
        self,
        user,
        timestamp: datetime.datetime,
        delta: datetime.timedelta = datetime.timedelta(seconds=5),
    ):
        near = self.bunch_near_date(user, timestamp, delta)
        if not near.exists():
            raise APIException(
                code=400, detail=_("Object with near date doesn't exists")
            )
        min_delta = 1e9
        min_object_date = None
        for object_with_date in near:
            difference = abs((object_with_date.created - timestamp).total_seconds())
            if difference < min_delta:
                min_object_date = object_with_date
                min_delta = difference
        return min_object_date
