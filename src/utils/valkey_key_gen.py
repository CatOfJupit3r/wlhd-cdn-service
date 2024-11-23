class ValkeyKeyGen:
    @staticmethod
    def translation_key(dlc: str, language: str) -> str:
        return f'translation-{dlc}-{language}'
