import uvicorn

import settings
import server


def start():
    uvicorn.run(server.app, host=settings.HOST, port=settings.PORT)
