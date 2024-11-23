from fastapi import APIRouter, Depends

from middlewares.authorize_token import authorize_token
from services.admin_service import AdminService

router = APIRouter()


@router.delete(
    "/cache",
    name='Deletes all cache',
    description="Deletes all cache across all services.",
    tags=["admin"],
    dependencies=[Depends(authorize_token)]
)
async def clear_cache():
    return await AdminService.clear_cache()
