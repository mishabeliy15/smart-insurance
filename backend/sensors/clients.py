from abc import ABC, abstractmethod
from collections import Counter

import requests

from insurance.settings import MYMAPPI_API_KEY


class BaseRoadAPIClient(ABC):
    def __init__(self, key: str):
        self.key = key

    @abstractmethod
    def get_speed_limit(self, lat: float, long: float) -> int:
        raise NotImplemented("Getting speed limit not implemented.")


class MyMappiRoadAPIClient(BaseRoadAPIClient):
    API_URL = "https://api.mymappi.com/"
    API_ROADS_LIMIT = f"{API_URL}v1/roads/speed-limit"

    def __init__(self, key=MYMAPPI_API_KEY):
        super(MyMappiRoadAPIClient, self).__init__(key)

    def get_roads(self, lat: float, lon: float) -> dict:
        params = {"apikey": self.key, "lat": lat, "lon": lon}
        response = requests.get(self.API_ROADS_LIMIT, params=params)
        response.raise_for_status()
        roads = response.json()["data"]
        return roads

    def get_speed_limit(self, lat: float, long: float) -> int:
        roads = self.get_roads(lat, long)
        speeds = [road.get("maxspeed") for road in roads]
        speeds = filter(None, speeds)
        speeds = Counter(map(int, speeds))
        max_speed = speeds.most_common(1)[0][0]
        return max_speed
