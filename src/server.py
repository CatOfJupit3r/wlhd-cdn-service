from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes import apply_routes
from services.valkey_service import ValkeyService

app = FastAPI()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # STARTUP. Connect to Valkey.
    await ValkeyService.connect()
    yield
    # SHUTDOWN. Disconnect from Valkey so that no error is thrown.
    await ValkeyService.disconnect()

apply_routes(app)
