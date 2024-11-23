import pathlib
from typing import List

from src.repositories.coordinator_repository import CoordinatorRepository


class _CoordinatorService:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_CoordinatorService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.coordinator_repository = CoordinatorRepository()

    def find_user_asset(self, subdir_list: List[str], filename: str) -> 'bytes | None':
        relative_path = pathlib.Path(*subdir_list)
        return self.coordinator_repository.get_user_asset(relative_path, filename)


CoordinatorService = _CoordinatorService()
