def image_type_to_media(image_type: str) -> str:
    match image_type:
        case 'png':
            return 'image/png'
        case 'jpeg':
            return 'image/jpeg'
        case 'svg':
            return 'image/svg+xml'
        case 'webp':
            return 'image/webp'
        case 'gif':
            return 'image/gif'
        case _:
            return 'image/png'
