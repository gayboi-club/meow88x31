from ..utils.colors import parse_color
from PIL import Image
from .base import Style


class DoubleStyle(Style):
    name = "double"

    def apply_border(self, image: Image.Image, border_color: str | tuple | None = None) -> Image.Image:
        if not border_color:
            return image.copy()
        w, h = image.size
        img = image.copy()
        pixels = img.load()
        base = parse_color(border_color) if isinstance(border_color, str) else border_color
        col = base + (255,)
        for x in range(w):
            for row in [0, 1, h - 2, h - 1]:
                if 0 <= row < h:
                    pixels[x, row] = col
        for y in range(h):
            for col_x in [0, 1, w - 2, w - 1]:
                if 0 <= col_x < w:
                    pixels[col_x, y] = col
        return img
