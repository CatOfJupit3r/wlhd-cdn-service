from typing import Tuple

from PIL import Image

from random import Random
from src.models.avatar import Avatar


SCALE = 40
AVATAR_WIDTH = 10
AVATAR_HEIGHT = 10
AVATAR_SIZE = (AVATAR_WIDTH * SCALE, AVATAR_HEIGHT * SCALE)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def mix_colors(color1, color2) -> Tuple[int, int, int]:
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return (r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2


def compose_avatar(avatar: Avatar) -> Image.Image:
    local_random = Random()
    local_random.seed(avatar.pattern)
    primary_color = hex_to_rgb(avatar.primary)
    secondary_color = hex_to_rgb(avatar.secondary)
    middle_color = mix_colors(primary_color, secondary_color)
    palette = [primary_color, middle_color, secondary_color]

    darkener = (65, 74, 76)
    darker_palette = [mix_colors(secondary_color, darkener), mix_colors(primary_color, darkener)]

    image = Image.new("RGB", AVATAR_SIZE)
    pixels = image.load()

    for y in range(AVATAR_HEIGHT):
        for x in range(AVATAR_WIDTH):
            color = local_random.choice(darker_palette) if x in {1, 2} else local_random.choice(palette)
            for i in range(SCALE):
                for j in range(SCALE):
                    pixels[x * SCALE + i, y * SCALE + j] = color

    return image
