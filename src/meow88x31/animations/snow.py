import random
import math
from PIL import Image
from .base import Animation
from ..core.frame import render_frame, CANVAS_W, CANVAS_H


class Flake:
    def __init__(self, pre_warm: bool = False):
        if pre_warm:
            self.y = random.uniform(0, CANVAS_H)
        else:
            self.y = random.uniform(-CANVAS_H, 0)
        self.x = random.uniform(0, CANVAS_W)
        self.speed = random.uniform(0.2, 0.7)
        self.drift = random.uniform(-0.3, 0.3)
        self.size = random.choice([1, 2])


class SnowAnimation(Animation):
    name = "snow"

    def generate(self, badge) -> list[Image.Image]:
        frames = []
        n_flakes = 20
        flakes = [Flake(pre_warm=True) for _ in range(n_flakes)]
        n_frames = 30
        warmup = 15

        for _ in range(warmup):
            for f in flakes:
                f.x = (f.x + f.drift) % CANVAS_W
                f.y += f.speed
                if f.y > CANVAS_H + 1:
                    f.y -= CANVAS_H + 1 + CANVAS_H

        for _ in range(n_frames):
            for f in flakes:
                f.x = (f.x + f.drift) % CANVAS_W
                f.y += f.speed
                if f.y > CANVAS_H + 1:
                    f.y -= CANVAS_H + 1 + CANVAS_H

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
            img = self._draw_flakes(img, flakes)
            frames.append(img)
        return frames

    def _draw_flakes(self, img: Image.Image, flakes: list) -> Image.Image:
        img = img.copy()
        pixels = img.load()
        for f in flakes:
            if 0 <= f.y <= CANVAS_H:
                white = (255, 255, 255, 255)
                for dx in range(f.size):
                    for dy in range(f.size):
                        px, py = int(f.x + dx), int(f.y + dy)
                        if 0 <= px < CANVAS_W and 0 <= py < CANVAS_H:
                            pixels[px, py] = white
        return img