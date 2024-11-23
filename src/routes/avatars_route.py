from fastapi import APIRouter, Response

from models.responses import ImageResponse
from src.models.avatar import Avatar
from src.services.avatars_service import AvatarsService

router = APIRouter()


# https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
@router.post(
    "/",
    name='Get and generate avatar',
    description="Gets the avatar image. If the avatar is missing, it tries to generate it using provided data.",
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
