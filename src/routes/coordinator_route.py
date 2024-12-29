from fastapi import APIRouter

from models.responses import NotFound, ImageResponse
from services.coordinator_service import CoordinatorService

assets_router = APIRouter(prefix='/coordinator/assets')
translations_router = APIRouter(prefix='/coordinator/translations')


@assets_router.get(
    "/{path_to_dir:path}",
    name='Get coordinator asset',
    description="Matches first best file using provided path.",
    responses={
        404: {
            "content": {"application/json": {}},
            "description": "Asset not found",
        },
    },
)
async def get_coordinator_asset(path_to_dir: str):
    subdir_list = path_to_dir.split('/')
    if len(subdir_list) == 0:
        raise NotFound()

    filename = subdir_list[-1]
    subdir_list.pop()

    matched, image_type = CoordinatorService.find_user_asset(subdir_list, filename)
    if matched is None:
        raise NotFound('Asset not found')
    return ImageResponse(matched, image_type)
