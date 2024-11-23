from fastapi import APIRouter, Response

from models.responses import ImageResponse
from src.models.avatar import Avatar
from src.services.avatars_service import AvatarsService

router = APIRouter()


# https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
@router.post(
    "/",
    name='Get avatar',
    description="Gets the avatar image.",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the avatar image",
        },
        404: {
            "content": {"application/json": {}},
            "description": "Avatar not found",
        },
    },
    response_class=Response
)
async def get_avatar(avatar: Avatar):
    image = AvatarsService.get_avatar(avatar)
    if image is None:
        return Response(status_code=404)
    return ImageResponse(image)


@router.post(
    "/",
    name='Generate avatar',
    description="Generates the avatar image.",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "Avatar generated",
        },
    },
    response_class=Response
)
async def generate_avatar(avatar: Avatar):
    AvatarsService.generate_avatar(avatar)
    return Response(status_code=200, content='Avatar was generated successfully')

