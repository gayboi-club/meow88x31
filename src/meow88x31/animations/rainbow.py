from PIL import Image
from .base import Animation
from ..core.frame import render_frame
from ..utils.colors import hsv_cycle


class RainbowAnimation(Animation):
    name = "rainbow"

    def generate(self, badge) -> list[Image.Image]:
        frames = []
        n_frames = 20
        for i in range(n_frames):
            fg = hsv_cycle(i, n_frames, 1.0, 1.0)
            fg_hex = f"#{fg[0]:02x}{fg[1]:02x}{fg[2]:02x}"
            img = render_frame(
                text=badge.text,
                style=badge.style,
                fg_color=fg_hex,
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
