from ..utils.colors import parse_color
from PIL import Image
from .base import Style


class FlatStyle(Style):
    name = "flat"

    def apply_border(self, image: Image.Image, border_color: str | tuple | None = None) -> Image.Image:
        if not border_color:
            return image.copy()
        w, h = image.size
        img = image.copy()
        pixels = img.load()
        base = parse_color(border_color) if isinstance(border_color, str) else border_color
        border = base + (255,)
        for x in range(w):
            pixels[x, 0] = border
            pixels[x, h - 1] = border
        for y in range(h):
            pixels[0, y] = border
            pixels[w - 1, y] = border
        return img
