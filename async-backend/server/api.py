from ai.head_pose_estimation import get_horizontal_angle
from aiohttp import ClientResponseError
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic.schema import UUID
from server.common import read_image_from_file, save_angle

router = APIRouter()


@router.get("/")
async def hello_world():
    return "Hello from AI!"


@router.post("/sensor/{sensor_id}/angle/")
async def head_horizontal_angle(
    sensor_id: UUID, image_file: UploadFile = File(..., alias="image")
):
    image = await read_image_from_file(image_file)
    angle, res_image = get_horizontal_angle(image, False)
    await save_angle(str(sensor_id), angle)
    return {"angle": angle}
