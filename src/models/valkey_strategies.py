import json
from abc import abstractmethod
from typing import Any, Dict

from ..models.exceptions import BadValkeyValueError


class iValkeyStrategy:
    @abstractmethod
    def execute(self, value: str | None) -> Any:
        pass


class StringValkeyStrategy(iValkeyStrategy):
    __slots__ = []
    def __init__(self): ...

    def execute(self, value: str | None) -> Any:
        return value


class JSONValkeyStrategy(iValkeyStrategy):
    __slots__ = []

    def __init__(self): ...

    def execute(self, value: str | None) -> Dict[str, Any]:
        if value is None or value == 'None':
            raise BadValkeyValueError()
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            raise BadValkeyValueError()
