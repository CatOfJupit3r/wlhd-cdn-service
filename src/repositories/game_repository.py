import pathlib
from os import getcwd

from utils import match_best_image_type

# :root/data/stored/installed
PATH_TO_DLCS = pathlib.Path(getcwd()) / 'data' / 'installed'
IGNORED_FOLDERS = ['__pycache__']


class GameRepository:
    def __init__(self, path_to_dlcs: pathlib.Path = None):
        if path_to_dlcs is not None and path_to_dlcs.exists():
            self.path_to_dlcs = path_to_dlcs
        else:
            self.path_to_dlcs = PATH_TO_DLCS
        self._list_of_dlcs = self.get_all_dlcs()

    @property
    def list_of_dlcs(self) -> list:
        if not self._list_of_dlcs:
            self._list_of_dlcs = self.get_all_dlcs()
        return self._list_of_dlcs

    def get_all_dlcs(self) -> list:
        return [d.name for d in self.path_to_dlcs.iterdir() if d.is_dir() and d.name not in IGNORED_FOLDERS]

    def get_game_asset(self, dlc: str, path: pathlib.Path, filename: str) -> 'None | bytes':
        if dlc not in self.list_of_dlcs:
            return None
        return match_best_image_type(self.path_to_dlcs / dlc / 'assets' / path, filename)
