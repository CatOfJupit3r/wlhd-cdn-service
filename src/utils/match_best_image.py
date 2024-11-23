import pathlib

# from top to bottom preferred assets
IMAGE_HIERARCHY = ['svg', 'webp', 'png', 'gif', 'jpg', 'jpeg']


def match_best_image_type(path_to_avatars: pathlib.Path, file_name: str) -> 'None | Bytes':
    if not path_to_avatars.exists(): # save 6 lookups
        return None

    for image in IMAGE_HIERARCHY:
        try:
            with open(path_to_avatars / f'{file_name}.{image}', 'rb') as file:
                return file.read()
        except FileNotFoundError:
            continue
    return None
