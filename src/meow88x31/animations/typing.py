import math
from PIL import Image
from .base import Animation
from ..core.frame import render_frame, CANVAS_W, CANVAS_H


class TypingAnimation(Animation):
    name = "typing"

    def generate(self, badge) -> list[Image.Image]:
        frames = []
        text = badge.text
        cursor = "_"
        for i in range(len(text) + 1):
            visible = text[:i]
            if i < len(text):
                display = visible + cursor
            else:
                display = visible
            for blink in range(4):
                d = display if blink % 2 == 0 else visible
                img = render_frame(
                    text=d,
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
                frames.append(img)
        return frames
