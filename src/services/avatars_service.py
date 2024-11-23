from PIL import Image

from src.models.avatar import Avatar
from src.repositories.avatars_repository import AvatarsRepository
from src.utils import compose_avatar


class _AvatarsService:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_AvatarsService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.avatars_repository = AvatarsRepository()

    def get_avatar(self, avatar: Avatar) -> Image.Image:
        avatar_file = self.avatars_repository.get(avatar.to_hash())
        if avatar_file is None:
            new_avatar = compose_avatar(avatar)
            self.avatars_repository.save(avatar.to_hash(), new_avatar)
            return new_avatar
        else:
            return avatar_file


AvatarsService = _AvatarsService()
