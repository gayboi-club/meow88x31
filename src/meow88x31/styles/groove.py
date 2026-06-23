from ..utils.colors import parse_color, lighten_color, darken_color
from PIL import Image
from .base import Style


class GrooveStyle(Style):
    name = "groove"

    def apply_border(self, image: Image.Image, border_color: str | tuple | None = None) -> Image.Image:
        if not border_color:
            return image.copy()
        w, h = image.size
        img = image.copy()
        pixels = img.load()
        base = parse_color(border_color) if isinstance(border_color, str) else border_color
        dark = darken_color(base, 0.4) + (255,)
        light = lighten_color(base, 0.6) + (255,)
        for y in range(h):
            pixels[0, y] = dark
            pixels[1, y] = light
            pixels[w - 2, y] = dark
            pixels[w - 1, y] = light
        for x in range(w):
            pixels[x, 0] = dark
            pixels[x, 1] = light
            pixels[x, h - 2] = dark
            pixels[x, h - 1] = light
        return img
