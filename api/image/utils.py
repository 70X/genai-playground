from typing import Literal
from PIL import Image
from io import BytesIO


def img_to_bytes(
    image: Image.Image, img_format: Literal["PNG", "JPEG"] = "PNG"
) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=img_format)
    return buffer.getvalue()


def save_image(
    image: Image.Image, path: str, img_format: Literal["PNG", "JPEG"] = "PNG"
) -> None:
    try:
        print(f"Saving image to {path}...")
        image.save(path, format=img_format)
    except Exception as e:
        print(f"Error saving image to {path}: {e}")
