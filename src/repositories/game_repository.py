import json
import pathlib
from os import getcwd
from typing import Dict, Any

from ..models.game_data import AllowedGameDataTypesEnum
from ..utils import match_best_image_type

# :root/data/stored/installed
PATH_TO_DLCS = pathlib.Path(getcwd()) / 'data' / 'installed'
IGNORED_FOLDERS = ['__pycache__']


class GameRepository:
    __slots__ = ['path_to_dlcs', '_list_of_dlcs', 'languages_aliases']

    def __init__(self, path_to_dlcs: pathlib.Path = None):
        if path_to_dlcs is not None and path_to_dlcs.exists():
            self.path_to_dlcs = path_to_dlcs
        else:
            self.path_to_dlcs = PATH_TO_DLCS
        self._list_of_dlcs = self.get_all_dlcs()
        self.languages_aliases = {}

    @property
    def list_of_dlcs(self) -> list:
        if not self._list_of_dlcs:
            self._list_of_dlcs = self.get_all_dlcs()
        return self._list_of_dlcs

    def get_all_dlcs(self) -> list:
        return [d.name for d in self.path_to_dlcs.iterdir() if d.is_dir() and d.name not in IGNORED_FOLDERS]

    def get_game_asset(self, dlc: str, path: pathlib.Path, filename: str) -> 'None | Tuple[bytes, str]':
        if dlc not in self.list_of_dlcs:
            return None
        return match_best_image_type(self.path_to_dlcs / dlc / 'assets' / path, filename)

    def get_translations(self, dlc: str, real_language: str) -> 'Dict[str, Any] | None':
        """
        Languages are stored in folders in many jsons
        They need to be read and merged into one dict

        Sometimes, language can't be found, but there is language from other region. 
        then we can safely assume that it's the same language

        Returned dict is compatible with the i18n library
        :param dlc: dlc name
        :param real_language: language code
        :return: dict with translations
        """
        path_to_dlc = self.path_to_dlcs / dlc / 'translations'
        if not path_to_dlc.exists():
            return None

        language_for_search = real_language
        if not (path_to_dlc / real_language).exists():
            language_for_search = self._find_first_best_fallback_language(path_to_dlc, real_language)

        translations = {}
        if language_for_search:
            translations = self._extract_language_files_from_path(path_to_dlc / language_for_search)

        return {
            real_language: {
                dlc: {
                    **translations
                }
            }
        }

    def _find_first_best_fallback_language(self, path_to_dlc_translations: pathlib.Path, language: str) -> 'str | None':
        """
        Finds first best fallback language
        :param path_to_dlc_translations: path to dlc translations
        :param language: language code
        :return: language code or None
        """
        if language in self.languages_aliases:  # if language is already in aliases
            return self.languages_aliases[language]
        language_code = language.split('_')[0]
        for lang in path_to_dlc_translations.iterdir():
            # if it's a directory, and it's the language we're looking for
            # maybe also check if it is empty?
            if lang.is_dir() and lang.name.startswith(language_code):
                self.languages_aliases[language] = lang.name
                return lang.name
        return None

    @staticmethod
    def _extract_language_files_from_path(path: pathlib.Path) -> Dict[str, Any]:
        """
        Extracts language files from path
        :param path: path to language files
        :return: dict with translations
        """
        result = {}

        for file in path.iterdir():
            if file.is_file():
                parsed = json.loads(file.read_text(encoding='utf-8'))
                result.update(parsed)

        return result

    def get_game_data_with_descriptor(self, dlc: str, data_type: AllowedGameDataTypesEnum,
                                      descriptor: str) -> 'Dict[str, Any] | None':
        """
        Returns game data for given dlc, data type and descriptor
        :param dlc: dlc name
        :param data_type: data type
        :param descriptor: descriptor
        :return: dict with game data
        """
        data = self.get_all_game_data(dlc, data_type)
        if data:
            return data.get(descriptor)
        return None

    def get_all_game_data(self, dlc: str, data_type: AllowedGameDataTypesEnum) -> Dict[str, Dict[str, Any]]:
        """
        Returns all game data for given dlc and data type
        :param dlc: dlc name
        :param data_type: data type
        :return: dict with game data
        """
        path_to_dlc = self.path_to_dlcs / dlc / 'data'
        if not path_to_dlc.exists():
            return {}
        return self.append_descriptor_to_game_data(self._extract_game_data_from_path(path_to_dlc, data_type), dlc)

    def append_descriptor_to_game_data(self, game_data: Dict[str, Any], dlc: str) -> Dict[str, Any]:
        """
        Appends descriptor to game data
        :param game_data: game data
        :param dlc: dlc name
        :return: game data with descriptor
        """
        if not game_data:
            return game_data
        for key, value in game_data.items():
            value.update({'descriptor': f"{dlc}:{key}"})
            game_data[key] = value
        return game_data

    def _extract_game_data_from_path(self, path_to_dlc_data: pathlib.Path, data_type: AllowedGameDataTypesEnum) -> Dict[
        str, Dict[str, Any]]:
        """
        Extracts game data from path
        :param path_to_dlc_data: path to game data
        :param data_type: data type
        :return: dict with game data
        """
        result = {}

        for file in path_to_dlc_data.iterdir():
            if file.is_dir():
                result.update(self._extract_game_data_from_path(file, data_type))
            elif file.is_file():
                if '.' not in file.name:  # edge case
                    continue
                contents, media_type = file.name.split('.')
                if media_type != "json":
                    continue
                if contents not in AllowedGameDataTypesEnum.keys():
                    continue
                try:
                    parsed = json.loads(file.read_text(encoding='utf-8'))
                    result.update(parsed)
                except json.JSONDecodeError:
                    continue

        return result
