import pathlib
from typing import List

from repositories.game_repository import GameRepository


class _GameService:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_GameService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.game_repository = GameRepository()

    def get_installed_dlcs(self) -> List[str]:
        return self.game_repository.list_of_dlcs

    def find_asset(self, dlc: str, subdir_list: List[str], filename: str) -> 'bytes | None':
        path = pathlib.Path(*subdir_list)
        return self.game_repository.get_game_asset(dlc, path, filename)

    def get_translations(self, dlc: str, languages: List[str]) -> 'dict | None':
        translations = {}
        for language in languages:
            translations.update(self.game_repository.get_translations(dlc, language))
        return translations


GameService = _GameService()
