from fastapi import FastAPI

from .game_routes import router as game_router
from .avatars_route import router as avatars_router
from .admin_route import router as admin_router
from .index_route import router as index_router


def apply_routes(app: FastAPI):
    app.include_router(index_router)
    app.include_router(avatars_router, prefix='/avatars')
    app.include_router(game_router, prefix='/game')
    app.include_router(admin_router, prefix='/admin')
