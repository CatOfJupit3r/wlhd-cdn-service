import json

from valkey.asyncio import Valkey
from valkey.exceptions import ConnectionError

import settings
from models.exceptions import BadValkeyValueError
from models.valkey_strategies import iValkeyStrategy, StringValkeyStrategy


class _ValkeyService:
    instance = None
    __slots__ = ['config', 'key_lifetime', 'connection']

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_ValkeyService, cls).__new__(cls)
        return cls.instance

    def __init__(self, key_lifetime: int = None):
        # Valkey configuration from settings
        self.connection = None
        self.config = {
            "host": settings.VALKEY_HOST,
            "port": settings.VALKEY_PORT,
            "db": settings.VALKEY_DB,
            "decode_responses": True,
        }
        self.key_lifetime = key_lifetime or settings.VALKEY_KEY_LIFETIME

    async def connect(self):
        if self.connection is None:
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

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def set_key(self, key: str, value: str) -> None:
        """
        Sets the key-value pair in Valkey.
        """
        if self.connection:
            await self.connection.set(
                key,
                value=json.dumps(value),
                ex=self.key_lifetime
            )

    async def get_key(self, key: str, strategy: iValkeyStrategy = None, delete_bad_key: bool = True):
        """
        Returns the value for the given key.
        """
        if self.connection:
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
        return None

    async def delete_key(self, key: str) -> None:
        """
        Deletes the key from the Valkey database.
        """
        if self.connection:
            await self.connection.delete(key)

    async def flush_db(self) -> None:
        """
        Flushes the Valkey database.
        """
        if self.connection:
            await self.connection.flushdb()


ValkeyService = _ValkeyService()
