from PIL import Image
from .base import Animation
from ..core.frame import render_frame, CANVAS_W, CANVAS_H


class ScanlineAnimation(Animation):
    name = "scanline"

    def generate(self, badge) -> list[Image.Image]:
        frames = []
        n_frames = CANVAS_H

        for offset in range(n_frames):
            img = render_frame(
                text=badge.text,
                style=badge.style,
                fg_color=badge.fg_color,
                bg_type=badge.bg_type,
                bg_color=badge.bg_color,
                bg_gradient=badge.bg_gradient,
                flag_name=badge.flag_name,
                border_color=badge.border_color,
                text_border_color=badge.text_border_color,
                text_border_width=badge.text_border_width,
                font_path=badge.font_path,
                font_size=badge.font_size,
                font_weight=badge.font_weight,
                fg_gradient=badge.fg_gradient,
                border_gradient=badge.border_gradient,
                gradient=badge.gradient,
                gradient_direction=badge.gradient_direction,
            )
            img = self._apply_scanlines(img, offset)
            frames.append(img)
        return frames

    def _apply_scanlines(self, img: Image.Image, offset: int) -> Image.Image:
        img = img.copy()
        pixels = img.load()
        for y in range(CANVAS_H):
            for x in range(CANVAS_W):
                c = pixels[x, y]
                if (y + offset) % 4 < 2:
                    factor = 0.65
                else:
                    factor = 1.0
                nr = int(c[0] * factor)
                ng = int(c[1] * factor)
                nb = int(c[2] * factor)
                pixels[x, y] = (min(nr, 255), min(ng, 255), min(nb, 255), c[3])
        return img
