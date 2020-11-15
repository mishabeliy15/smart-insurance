import datetime
import random
import traceback
from argparse import ArgumentParser
from glob import glob
from time import sleep
from typing import List
from uuid import UUID

import requests
from requests import HTTPError

DEFAULT_DATA_PATH = "./../mock_data/*.jpg"
NORMAL_ANGLE_PATH = "./../mock_data/normal.jpg"
SENSOR_API_URL = "http://localhost/ai/sensor/{!s}/angle/"


def validate_uuid(string: str) -> str:
    UUID(string)
    return string


def return_to_normal():
    return random.choice([True, False])


def format_print_file(path: str):
    short_path = path.split("/")[-1]
    print(f"[{datetime.datetime.now().time()}] File: {short_path}", end=" ")


def main(sensor_id: str, image_files_path: str):
    image_files = find_files(image_files_path)
    while True:
        for image_path in image_files:
            format_print_file(image_path)
            try:
                angle = make_angle_request(sensor_id, image_path)
                print(f"Angle: {angle}")
                if return_to_normal():
                    sleep(random.randint(2, 5))
                    format_print_file(NORMAL_ANGLE_PATH)
                    angle = make_angle_request(sensor_id, image_path)
                    print(f"Angle: {angle}")
            except HTTPError as exc:
                print()
                traceback.print_exc()
                print(exc.response.json())
            sleep(1)


def find_files(path: str) -> List[str]:
    files = glob(path)
    return files


def make_angle_request(sensor_id: str, path: str) -> int:
    url = SENSOR_API_URL.format(sensor_id)
    with open(path, "rb") as image_file:
        response = requests.post(url, files={"image": image_file})
    response.raise_for_status()
    return response.json()["angle"]


if __name__ == "__main__":
    parser = ArgumentParser(description="Mock speed sensor")
    parser.add_argument(
        "--uuid",
        "-id",
        dest="uuid",
        required=True,
        help="UUID of camera angle sensor",
        type=validate_uuid,
    )
    parser.add_argument(
        "--path",
        "-p",
        dest="path",
        default=DEFAULT_DATA_PATH,
        required=False,
        help="Path to photos",
    )
    args = parser.parse_args()
    main(args.uuid, args.path)
