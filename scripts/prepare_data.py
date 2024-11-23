import pathlib
from os import getcwd

DATA_FOLDER = pathlib.Path(getcwd()) / 'data'

REQUIRED_FOLDERS = [
    pathlib.Path('stored') / 'avatars',
    pathlib.Path('stored') / 'assets',
    pathlib.Path('installed')
]


def prepare_data() -> None:
    """
    Prepares :root/data folder for the application to work properly.
    """
    for folder in REQUIRED_FOLDERS:
        folder_path = DATA_FOLDER / folder
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            with open(folder_path / '.gitkeep', 'w+') as file:
                file.write('')
            print(f'Folder {folder} created.')
        else:
            print(f'Folder {folder} already exists.')
    print('Data preparation finished.')