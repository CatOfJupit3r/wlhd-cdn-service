from http import HTTPStatus
from io import BytesIO

from fastapi import Response, HTTPException
from PIL import Image

from ..utils import image_type_to_media


# https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
class ImageResponse(Response):
    def __init__(self, image: Image.Image | bytes, image_type: str, **kwargs):
        converted: BytesIO
        if isinstance(image, Image.Image):
            converted = self._convert_pil_image(image)
        elif isinstance(image, bytes):
            converted = self._convert_bytes(image)
        else:
            raise Exception(f'Bad type matching for ImageResponse. Got type: {type(image)}')

        super().__init__(
            **kwargs,
            media_type=image_type_to_media(image_type) or "image/png",
            content=converted.getvalue()
        )

    @staticmethod
    def _convert_pil_image(image: Image.Image) -> BytesIO:
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @staticmethod
    def _convert_bytes(image: bytes) -> BytesIO:
        return BytesIO(image)


def NotFound(content: str = 'Content cannot not found!') -> HTTPException:
    return HTTPException(detail=content, status_code=HTTPStatus.NOT_FOUND)
