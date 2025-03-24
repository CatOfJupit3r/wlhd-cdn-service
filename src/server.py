from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import routes
from .services.valkey_service import ValkeyService


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # STARTUP. Connect to Valkey.
    await ValkeyService.connect()
    yield
    # SHUTDOWN. Disconnect from Valkey so that no error is thrown.
    await ValkeyService.disconnect()


app = FastAPI(
    lifespan=lifespan
)

routes.apply_routes(app)
