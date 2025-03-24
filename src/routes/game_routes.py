from fastapi import APIRouter

from ..services.game_service import GameService
from .coordinator_route import assets_router as coordinator_assets_router, \
    translations_router as coordinator_translations_router
from .dlc_route import assets_router as dlc_assets_router, translations_router as dlc_translations_router

router = APIRouter()


@router.get(
    "/",
    name='Get all installed DLCs',
    description="Returns all installed DLCs.",
    tags=["game"]
)
def get_all_dlcs():
    return {"installed": GameService.get_installed_dlcs()}


router.include_router(coordinator_assets_router, tags=["coordinator"])
router.include_router(coordinator_translations_router, tags=["coordinator"])

router.include_router(dlc_assets_router, tags=["dlc"])
router.include_router(dlc_translations_router, tags=["dlc"])
