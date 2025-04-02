from typing import Annotated

from fastapi import APIRouter, Response
from fastapi.params import Query, Depends

import settings
from ..middlewares.authorize_token import auth_middleware
from ..models.responses import ImageResponse
from ..models.avatar import Avatar
from ..services.avatars_service import AvatarsService

router = APIRouter()

PatternQueryType = Annotated[str, Query(max_length=64)]
PrimaryColorQueryType = Annotated[str, Query(max_length=7, regex='^#[0-9A-Fa-f]{6}$')]
SecondaryColorQueryType = Annotated[str, Query(max_length=7, regex='^#[0-9A-Fa-f]{6}$')]


@router.get(
    "",
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
async def get_avatar(
        pattern: PatternQueryType,
        primary: PrimaryColorQueryType,
        secondary: SecondaryColorQueryType
):
    # to adhere to the API standards, we get the avatar image from query params and not from body. bruh
    avatar = Avatar(
        pattern=pattern,
        primary=primary,
        secondary=secondary
    )
    image = AvatarsService.get_avatar(avatar)
    if image is None:
        return Response(status_code=404)
    return ImageResponse(image, image_type='png')


@router.post(
    "",
    name='Generate avatar',
    description="Generates the avatar image.",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the avatar image",
        },
    },
    response_class=Response,
    dependencies=[Depends(auth_middleware(token=settings.COORDINATOR_TOKEN))]
)
async def generate_avatar(avatar: Avatar):
    AvatarsService.generate_avatar(avatar)
    return ImageResponse(AvatarsService.get_avatar(avatar), 'webp')
