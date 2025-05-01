import pathlib
from typing import List, Dict, Any

from ..models.game_data import AllowedGameDataTypesEnum
from ..repositories.game_repository import GameRepository


class _GameService:
    instance = None
    __slots__ = ['game_repository']

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_GameService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.game_repository = GameRepository()

    def get_installed_dlcs(self) -> List[str]:
        return self.game_repository.list_of_dlcs

    def find_asset(self, dlc: str, subdir_list: List[str], filename: str) -> 'Tuple[bytes, str] | None':
        path = pathlib.Path(*subdir_list)
        return self.game_repository.get_game_asset(dlc, path, filename)

    def get_translation(self, dlc: str, language: str) -> 'dict | None':
        return self.game_repository.get_translations(dlc, language)

    @staticmethod
    def get_descriptor_from_game_data(data: Dict[str, Any], descriptor: str) -> 'Dict[str, Any] | None':
        return data.get(descriptor)

    def get_game_all_data(self, dlc: str, data_type: AllowedGameDataTypesEnum) -> 'Dict[str, Any] | None':
        return self.game_repository.get_all_game_data(dlc, data_type)


GameService = _GameService()
