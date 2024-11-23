from fastapi import APIRouter
from models.responses import NotFound, ImageResponse
from services.game_service import GameService

assets_router = APIRouter(prefix='/{dlc}/assets')
translations_router = APIRouter(prefix='/{dlc}/translations')


"""

These routes are used to match DLC data by keys.
However, if dlc is `coordinator`, then it is handled by `coordinator_route.py` routes

"""


@assets_router.get(
    "/{path_to_dir:path}",
    name='Get DLC asset',
    description="Matches first best file using provided path.",
    responses={
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {},
                "image/svg+xml": {},
                "image/webp": {},
                "image/gif": {},
            },
        },
        404: {
            "content": {"application/json": {}},
            "description": "Asset not found",
        },
    },
)
async def get_dlc_asset(dlc: str, path_to_dir: str):
    subdir_list = path_to_dir.split('/')
    if len(subdir_list) == 0:
        raise NotFound()

    filename = subdir_list[-1]
    subdir_list.pop()

    matched = GameService.find_asset(dlc, subdir_list, filename)
    if matched is None:
        raise NotFound('Asset not found')
    return ImageResponse(matched)
