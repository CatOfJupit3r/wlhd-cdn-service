class ValkeyKeyGen:
    @staticmethod
    def translation_key(dlc: str, language: str) -> str:
        return f'translation-{dlc}-{language}'

    @staticmethod
    def game_data_key_with_descriptor(dlc: str, data_type: str, descriptor: str) -> str:
        return f'game-data-{dlc}-{data_type}-{descriptor}'

    @staticmethod
    def game_data_key(dlc: str, data_type: str) -> str:
        return f'game-data-{dlc}-{data_type}'
