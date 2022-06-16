import cv2
import numpy as np

from aiohttp import ClientResponseError, ClientSession
from fastapi import HTTPException, UploadFile
from settings import ANGLE_API_URL


def read_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    image = np.asarray(bytearray(image_bytes), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


async def read_image_from_file(image_file: UploadFile) -> np.ndarray:
    image_bytes = await image_file.read()
    image = read_image_from_bytes(image_bytes)
    return image


async def save_angle(sensor_id: str, angle: int):
    data = {"sensor": sensor_id, "angle": angle}
    async with ClientSession() as session:
        async with session.post(ANGLE_API_URL, json=data) as resp:
            detail = await resp.json()
            try:
                resp.raise_for_status()
            except ClientResponseError:
                raise HTTPException(status_code=resp.status, detail=detail["detail"])
