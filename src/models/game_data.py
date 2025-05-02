from enum import Enum
from typing import List


class AllowedGameDataTypesEnum(str, Enum):
    characters = 'characters'
    status_effects = 'status-effects'
    area_effects = 'area-effects'
    spells = 'spells'
    items = 'items'
    weapons = 'weapons'

    @classmethod
    def keys(cls) -> List[str]:
        return [item.value for item in cls]


class AllGameDataFlagsEnum(str, Enum):
    all = 'all'
    info = 'info'
    