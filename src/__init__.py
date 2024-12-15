import uvicorn

import settings
from .server import app


def start():
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
