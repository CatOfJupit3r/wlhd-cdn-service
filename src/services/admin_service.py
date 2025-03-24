import traceback

import settings
from ..services.valkey_service import ValkeyService


class _AdminService:
    instance = None
    __slots__ = ['admin_token']

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_AdminService, cls).__new__(cls)
        return cls.instance

    def __init__(self, admin_token: str = None):
        if admin_token is not None:
            self.admin_token = admin_token
        else:
            self.admin_token = settings.ADMIN_TOKEN

    @staticmethod
    async def clear_cache():
        try:
            await ValkeyService.flush_db()
            return {"status": "Cache was cleared successfully"}
        except Exception as _:
            traceback.print_exc()
            return {"status": f"Failed to clear cache"}


AdminService = _AdminService()
