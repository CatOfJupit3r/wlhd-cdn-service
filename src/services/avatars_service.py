from PIL import Image

from ..models.avatar import Avatar
from ..repositories.avatars_repository import AvatarsRepository
from ..utils import compose_avatar


class _AvatarsService:
    instance = None
    __slots__ = ['avatars_repository']

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_AvatarsService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.avatars_repository = AvatarsRepository()

    def get_avatar(self, avatar: Avatar) -> Image.Image:
        return self.avatars_repository.get(avatar.to_hash())

    def generate_avatar(self, avatar: Avatar) -> Image.Image:
        new_avatar = compose_avatar(avatar)
        self.avatars_repository.save(avatar.to_hash(), new_avatar)
        return new_avatar


AvatarsService = _AvatarsService()
