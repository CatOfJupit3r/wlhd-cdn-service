import json

from valkey.asyncio import Valkey
from valkey.exceptions import ConnectionError

import settings
from ..models.exceptions import BadValkeyValueError
from ..models.valkey_strategies import iValkeyStrategy, StringValkeyStrategy


def with_connection(func):
    async def wrapper(self, *args, **kwargs):
        if _ValkeyService.instance.connection is None:
            return None
        return await func(self, *args, **kwargs)
    return wrapper


class _ValkeyService:
    instance = None
    __slots__ = ['config', 'key_lifetime', 'connection']

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_ValkeyService, cls).__new__(cls)
        return cls.instance

    def __init__(self, key_lifetime: int = None):
        # Valkey configuration from settings
        self.connection: None | Valkey = None
        self.config = {
            "host": settings.VALKEY_HOST,
            "port": settings.VALKEY_PORT,
            "db": settings.VALKEY_DB,
            "decode_responses": True,
        }
        self.key_lifetime = key_lifetime or settings.VALKEY_KEY_LIFETIME
    
    @with_connection
    async def connect(self):
        if self.connection is not None:
            return
        try:
            print("Attempting to connect to Valkey...")
            self.connection = Valkey(**self.config)
            # Test connection
            await self.connection.ping()
            print("Successfully connected to Valkey.")
        except (ConnectionError, ConnectionRefusedError) as e:
            print(f"Failed to connect to Valkey: {e}")
            print("WARNING: Running in no-cache mode.")
            self.connection = None

    @with_connection
    async def disconnect(self):
        await self.connection.close()
        self.connection = None
    
    @with_connection
    async def set_key(self, key: str, value: str) -> None:
        """
        Sets the key-value pair in Valkey.
        """
        await self.connection.set(
            key,
            value=json.dumps(value),
            ex=self.key_lifetime
        )
    
    @with_connection
    async def get_key(self, key: str, strategy: iValkeyStrategy = None, delete_bad_key: bool = True):
        """
        Returns the value for the given key.
        """
        value = await self.connection.get(key)
        try:
            if strategy:
                return strategy.execute(value)
            else:
                return StringValkeyStrategy().execute(value)
        except BadValkeyValueError:
            if delete_bad_key:
                await self.delete_key(key)
            return None

    @with_connection
    async def delete_key(self, key: str) -> None:
        """
        Deletes the key from the Valkey database.
        """
        await self.connection.delete(key)
    
    @with_connection
    async def flush_db(self) -> None:
        """
        Flushes the Valkey database.
        """
        await self.connection.flushdb()


ValkeyService = _ValkeyService()
