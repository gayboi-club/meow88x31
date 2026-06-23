from typing import Callable
from PIL import Image

from .frame import render_frame, CANVAS_W, CANVAS_H


class Badge:
    def __init__(
        self,
        text: str,
        style=None,
        fg_color: str = "white",
        bg_type: str = "solid",
        bg_color: str = "#336699",
        bg_gradient: list | None = None,
        flag_name: str | None = None,
        border_color: str | tuple | None = None,
        text_border_color: str | tuple | None = None,
        text_border_width: int = 1,
        font_path: str | None = None,
        font_size: int = 0,
        font_weight: int = 400,
        fg_gradient: list | None = None,
        border_gradient: list | None = None,
        gradient: list | None = None,
        gradient_direction: str = "horizontal",
    ):
        self.text = text
        self.style = style
        self.fg_color = fg_color
        self.bg_type = bg_type
        self.bg_color = bg_color
        self.bg_gradient = bg_gradient
        self.flag_name = flag_name
        self.border_color = border_color
        self.text_border_color = text_border_color
        self.text_border_width = text_border_width
        self.font_path = font_path
        self.font_size = font_size
        self.font_weight = font_weight
        self.fg_gradient = fg_gradient
        self.border_gradient = border_gradient
        self.gradient = gradient
        self.gradient_direction = gradient_direction

    def render_static(self) -> Image.Image:
        return render_frame(
            text=self.text,
            style=self.style,
            fg_color=self.fg_color,
            bg_type=self.bg_type,
            bg_color=self.bg_color,
            bg_gradient=self.bg_gradient,
            flag_name=self.flag_name,
            border_color=self.border_color,
            text_border_color=self.text_border_color,
            text_border_width=self.text_border_width,
            font_path=self.font_path,
            font_size=self.font_size,
            font_weight=self.font_weight,
            fg_gradient=self.fg_gradient,
            border_gradient=self.border_gradient,
            gradient=self.gradient,
            gradient_direction=self.gradient_direction,
        )

    def render_animated(self, animation) -> list[Image.Image]:
        return animation.generate(self)

    def save(self, path: str, frames: list[Image.Image] | None = None):
        if frames and len(frames) > 1:
            frames[0].save(
                path,
                save_all=True,
                append_images=frames[1:],
                duration=100,
                loop=0,
                disposal=2,
            )
        else:
            img = frames[0] if frames else self.render_static()
            img.save(path)
