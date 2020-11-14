import cv2

from ai.head_pose_estimation import get_horizontal_angle
from fastapi import APIRouter, File, UploadFile, Response, Form
from server.common import read_image_from_file

router = APIRouter()


@router.post("/angle/image/")
async def head_horizontal_angle(image_file: UploadFile = File(..., alias="image")):
    image = await read_image_from_file(image_file)
    angle, res_image = get_horizontal_angle(image, True)
    _, res_image_file = cv2.imencode(".png", res_image)
    res_image_file = res_image_file.tostring()
    return Response(content=res_image_file, media_type="image/png")


@router.post("/angle/")
async def head_horizontal_angle(image_file: UploadFile = File(..., alias="image")):
    image = await read_image_from_file(image_file)
    angle, res_image = get_horizontal_angle(image, False)
    return {"angle": angle}
