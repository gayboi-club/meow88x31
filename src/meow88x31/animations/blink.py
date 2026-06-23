from PIL import Image
from .base import Animation
from ..core.frame import render_frame


class BlinkAnimation(Animation):
    name = "blink"

    def generate(self, badge) -> list[Image.Image]:
        frames = []
        for i in range(8):
            show = i % 2 == 0
            img = render_frame(
                text=badge.text if show else "",
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
