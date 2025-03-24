from fastapi import APIRouter, Depends

import settings
from ..middlewares.authorize_token import auth_middleware
from ..services.admin_service import AdminService

router = APIRouter()


@router.delete(
    "/cache",
    name='Deletes all cache',
    description="Deletes all cache across all services.",
    tags=["admin"],
    dependencies=[Depends(auth_middleware(token=settings.ADMIN_TOKEN))]
)
async def clear_cache():
    return await AdminService.clear_cache()
