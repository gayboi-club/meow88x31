from PIL import Image
from .base import Style


class NoBorderStyle(Style):
    name = "none"

    def apply_border(self, image: Image.Image, border_color: str | tuple | None = None) -> Image.Image:
        return image.copy()
