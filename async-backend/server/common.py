from tempfile import NamedTemporaryFile

import cv2
import numpy as np
from fastapi import UploadFile


def read_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    with NamedTemporaryFile() as temp_file:
        temp_file.write(image_bytes)
        temp_file.flush()
        temp_file.seek(0)
        image = cv2.imread(temp_file.name)
    return image


async def read_image_from_file(image_file: UploadFile) -> np.ndarray:
    image_bytes = await image_file.read()
    image = read_image_from_bytes(image_bytes)
    return image
