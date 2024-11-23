import pathlib
from os import getcwd

from utils import match_best_image_type

# :root/data/stored
PATH_TO_COORDINATOR_ASSETS = pathlib.Path(getcwd()) / 'data' / 'stored'
IGNORED_FOLDERS = ['__pycache__']


class CoordinatorRepository:
    __slots__ = ['path_to_dlcs']

    def __init__(self, path_to_coordinator_assets: pathlib.Path = None):
        if path_to_coordinator_assets is not None and path_to_coordinator_assets.exists():
            self.path_to_dlcs = path_to_coordinator_assets
        else:
            self.path_to_dlcs = PATH_TO_COORDINATOR_ASSETS

    def build_path(self, *args) -> pathlib.Path:
        return self.path_to_dlcs / pathlib.Path(*args)

    def get_user_asset(self, path: pathlib.Path, filename: str) -> 'None | bytes':
        if filename == '.gitkeep':
            return None
        return match_best_image_type(self.path_to_dlcs / 'assets' / path, filename)
