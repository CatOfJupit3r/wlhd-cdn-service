import src

import settings

if __name__ == '__main__':
    if not settings.SKIP_PREPARE:
        from scripts.prepare_data import prepare_data
        prepare_data()

    src.start()
