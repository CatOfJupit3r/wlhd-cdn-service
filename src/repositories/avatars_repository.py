import pathlib
from os import getcwd

from PIL import Image

# :root/data/stored/avatars
PATH_TO_AVATARS = pathlib.Path(getcwd()) / 'data' / 'stored' / 'avatars'


class AvatarsRepository:
    def __init__(self, path_to_avatars: pathlib.Path = None):
        if path_to_avatars is not None and path_to_avatars.exists():
            self.path_to_avatars = path_to_avatars
        else:
            self.path_to_avatars = PATH_TO_AVATARS

    def get(self, hashed: str) -> 'None | Image.Image':
        try:
            return Image.open(self.path_to_avatars / f'{hashed}.png')
        except FileNotFoundError:
            return None

    def save(self, hashed: str, file: Image.Image) -> None:
        file.save(self.path_to_avatars / f'{hashed}.png', format='PNG')
