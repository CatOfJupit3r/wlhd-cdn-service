from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Path

from models.responses import NotFound, ImageResponse
from services.game_service import GameService

assets_router = APIRouter(prefix='/{dlc}/assets')
translations_router = APIRouter(prefix='/{dlc}/translations')

DlcInPathType = Annotated[str, Path(regex='^[a-z]+$')]

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
async def get_dlc_asset(dlc: DlcInPathType, path_to_dir: str):
    subdir_list = path_to_dir.split('/')
    if len(subdir_list) == 0:
        raise NotFound()

    filename = subdir_list[-1]
    subdir_list.pop()

    matched = GameService.find_asset(dlc, subdir_list, filename)
    if matched is None:
        raise NotFound('Asset not found')
    return ImageResponse(matched)


@translations_router.get(
    "",
    name='Get DLC asset',
    description="Matches first best file using provided path.",
    responses={
        200: {
            "application/json": {},
            "description": "Return the translation file",
        },
        404: {
            "content": {"application/json": {}},
            "description": "Asset not found",
        },
    },
)
def get_dlc_translation(dlc: DlcInPathType, languages: Annotated[str, Query(max_length=64, regex='^([a-z]{2}_[A-Z]{2})(,[a-z]{2}_[A-Z]{2})*$')] = 'en_US'):
    languages_list = languages.split(',')
    translation = GameService.get_translations(dlc, languages_list)
    if translation is None:
        raise NotFound('Translation not found')
    return translation
