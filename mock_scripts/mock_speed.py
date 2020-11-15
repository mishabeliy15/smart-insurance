import datetime
import random
import traceback
from argparse import ArgumentParser
from collections import namedtuple
from time import sleep
from typing import List
from uuid import UUID

import requests
from requests import HTTPError

Point = namedtuple("Point", ["latitude", "longitude"])

DEFAULT_FILE_CORDS = "./coords.txt"
SENSOR_API_URL = "http://localhost/api/v0/speeds/"
MAX_ACCELERATION = 10


def validate_uuid(string: str) -> str:
    UUID(string)
    return string


def make_request(sensor_id: str, speed: int, point: Point):
    data = {
        "sensor": sensor_id,
        "speed": speed,
        "location": {"latitude": point.latitude, "longitude": point.longitude},
    }
    response = requests.post(SENSOR_API_URL, json=data)
    response.raise_for_status()


def main(sensor_id: str, coord_path: str):
    coords = load_coords(coord_path)
    n = len(coords)
    speed = i = 0
    iter_sign = 1
    acceleration_variants = [[1] * 65 + [-1] * 35, [-1] * 65 + [1] * 35]
    sign_choices = acceleration_variants[0]
    while True:
        point = coords[i]
        print(
            f"[{datetime.datetime.now().time()}] "
            f"Speed: {speed} Coords: {point.latitude}, {point.longitude}"
        )
        try:
            make_request(sensor_id, speed, point)
        except HTTPError as exc:
            traceback.print_exc()
            print(exc.response.json())

        sleep(1)

        acceleration = random.randint(1, MAX_ACCELERATION)
        if speed > 50:
            if speed > 120:
                sign_choices = acceleration_variants[1]
            elif speed < 60:
                sign_choices = acceleration_variants[0]

            acceleration *= random.choice(sign_choices)
        speed += acceleration

        if i + iter_sign == n or i + iter_sign < 0:
            iter_sign *= -1

        i += iter_sign


def load_coords(path: str) -> List[Point]:
    coords = []
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        line = line.split(",")
        point = Point(float(line[0]), float(line[1]))
        coords.append(point)
    return coords


if __name__ == "__main__":
    parser = ArgumentParser(description="Mock speed sensor")
    parser.add_argument(
        "--uuid",
        "-id",
        dest="uuid",
        required=True,
        help="UUID of speed sensor",
        type=validate_uuid,
    )
    parser.add_argument(
        "--path",
        "-p",
        dest="path",
        default=DEFAULT_FILE_CORDS,
        required=False,
        help="Path to coords",
    )
    args = parser.parse_args()
    main(args.uuid, args.path)
