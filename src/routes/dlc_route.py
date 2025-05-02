from typing import Annotated, List, Dict, Any

from fastapi import APIRouter, Query
from fastapi.params import Path

from ..models.game_data import AllowedGameDataTypesEnum, AllGameDataFlagsEnum
from ..models.responses import NotFound, ImageResponse
from ..models.valkey_strategies import JSONValkeyStrategy
from ..services.game_service import GameService
from ..services.valkey_service import ValkeyService
from ..utils import ValkeyKeyGen

assets_router = APIRouter(prefix='/{dlc}/assets')
translations_router = APIRouter(prefix='/{dlc}/translations')
game_data_router = APIRouter(prefix='/{dlc}/game_data')

DlcInPathType = Annotated[str, Path(pattern='^[a-z]+$')]
DescriptorsListType = Annotated[str | None, Query(max_length=256, pattern='^[a-z._-]+(,[a-z._-]+)*$')]
LanguagesListInQueryType = Annotated[
    str | None, Query(max_length=64, pattern='^([a-z]{2}_[A-Z]{2})(,[a-z]{2}_[A-Z]{2})*$')]

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

    asset = GameService.find_asset(dlc, subdir_list, filename)
    if asset is None:
        raise NotFound('Asset not found')
    matched, media_type = asset
    return ImageResponse(matched, image_type=media_type)


@translations_router.get(
    "",
    name='Get translations for DLC.',
    description="Provides all available translations for the DLC. If specified, returns only for the given languages.",
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
async def get_dlc_translation(dlc: DlcInPathType, languages: LanguagesListInQueryType = 'en_US'):
    languages_list = languages.split(',') if languages else []
    translations = {}

    for lang in languages_list:
        valkey_key = ValkeyKeyGen.translation_key(dlc, lang)
        cached = await ValkeyService.get_key(valkey_key, strategy=JSONValkeyStrategy())
        if cached:
            translations.update(cached)
            continue

        translation_file = GameService.get_translation(dlc, lang)
        if translation_file:
            translations.update(translation_file)
            await ValkeyService.set_key(valkey_key, translation_file)

    return translations


ALLOWED_KEYS_IN_SHORT_VARIANT = [
    'descriptor',
    'decorations',
]


def _prepare_game_data(game_data: Dict[str, Any], descriptors: List[str], variant: AllGameDataFlagsEnum):
    if len(descriptors) > 0:
        result = {x: GameService.get_descriptor_from_game_data(game_data, x) for x in descriptors}
    else:
        result = game_data

    if variant == AllGameDataFlagsEnum.all:
        return result
    elif variant == AllGameDataFlagsEnum.info:
        return {x: {k: v for k, v in result[x].items() if k in ALLOWED_KEYS_IN_SHORT_VARIANT} for x in result}
    return result


@game_data_router.get(
    "/{data_type}",
    name='Get ALL DLC game data of specific type (or array of descriptors if provided with query)',
    description="Matches all known game pieces using provided inputs and returns full, raw data in JSON format.",
    responses={
        202: {
            "content": {"application/json": {}},
            "description": "Return the game data",
        },
        404: {
            "content": {"application/json": {}},
            "description": "Game data not found",
        },
    },
)
async def get_all_dlc_game_data(
        dlc: DlcInPathType,
        data_type: AllowedGameDataTypesEnum,
        descriptors: DescriptorsListType = None,
        variant: AllGameDataFlagsEnum = AllGameDataFlagsEnum.all,
):
    processed_descriptors = descriptors.split(',') if descriptors else []

    valkey_key = ValkeyKeyGen.game_data_key(dlc, data_type)
    cached = await ValkeyService.get_key(valkey_key, strategy=JSONValkeyStrategy())
    if cached:
        return _prepare_game_data(cached, processed_descriptors, variant)

    game_data = GameService.get_game_all_data(dlc, data_type)
    if game_data is None:
        raise NotFound('Game data not found')
    await ValkeyService.set_key(valkey_key, game_data)

    return _prepare_game_data(game_data, processed_descriptors, variant)


@game_data_router.get(
    "/{data_type}/{descriptor}",
    name='Get DLC game data of specific type under descriptor',
    description="Matches first best game piece using provided inputs and returns full, raw data in JSON format.",
    responses={
        202: {
            "content": {"application/json": {}},
            "description": "Return the game data",
        },
        404: {
            "content": {"application/json": {}},
            "description": "Game data not found",
        },
    },
)
async def get_dlc_game_data(dlc: DlcInPathType, data_type: AllowedGameDataTypesEnum, descriptor: str):
    valkey_key_specific = ValkeyKeyGen.game_data_key_with_descriptor(dlc, data_type, descriptor)
    cached = await ValkeyService.get_key(valkey_key_specific, strategy=JSONValkeyStrategy())
    if cached:
        return cached

    valkey_key_general = ValkeyKeyGen.game_data_key(dlc, data_type)
    cached = await ValkeyService.get_key(valkey_key_general, strategy=JSONValkeyStrategy())
    if cached:
        in_cached = GameService.get_descriptor_from_game_data(cached, descriptor)
        if in_cached:
            await ValkeyService.set_key(valkey_key_specific, in_cached)
            return in_cached
        raise NotFound('Game data not found')

    all_data = GameService.get_game_all_data(dlc, data_type) or {}
    if all_data is None:
        raise NotFound('Game data not found')

    await ValkeyService.set_key(valkey_key_general, all_data)
    data = GameService.get_descriptor_from_game_data(all_data, descriptor)
    if data is None:
        raise NotFound('Game data not found')
    await ValkeyService.set_key(valkey_key_specific, data)
    return data
