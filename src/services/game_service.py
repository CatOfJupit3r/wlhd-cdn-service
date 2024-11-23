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
        self.avatars_repository = GameRepository()

    def get_installed_dlcs(self) -> List[str]:
        return self.avatars_repository.list_of_dlcs

    def find_asset(self, dlc: str, subdir_list: List[str], filename: str) -> 'bytes | None':
        path = pathlib.Path(*subdir_list)
        return self.avatars_repository.get_game_asset(dlc, path, filename)


GameService = _GameService()
