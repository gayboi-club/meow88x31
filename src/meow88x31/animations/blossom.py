import math
import random
from PIL import Image
from .base import Animation
from ..core.frame import render_frame, CANVAS_W, CANVAS_H


_PETAL_COLORS = ["#FFB7C5", "#FF9EB5", "#FF8FA3", "#FFC0CB"]
CYCLE = 64


class Petal:
    def __init__(self, n_frames: int):
        self.phase = random.uniform(0, 1)
        self.x = random.uniform(0, CANVAS_W)
        self.speed_y = CYCLE / n_frames
        self.speed_x = random.uniform(-0.2, 0.2)
        self.wobble_offset = random.uniform(0, 6.28)
        self.wobble_speed = random.uniform(0.1, 0.3)
        self.size = random.choice([1, 2])
        self.color = random.choice(_PETAL_COLORS)

    def y_at(self, frame: int) -> float:
        return ((self.phase * CYCLE + self.speed_y * frame) % CYCLE) - CANVAS_H

    def x_at(self, frame: int) -> float:
        return (self.x + self.speed_x * frame + math.sin(self.wobble_offset + self.wobble_speed * frame) * 0.3) % CANVAS_W


class BlossomAnimation(Animation):
    name = "blossom"

    def generate(self, badge) -> list[Image.Image]:
        n_frames = 30
        n_petals = 12
        petals = [Petal(n_frames) for _ in range(n_petals)]
        frames = []

        for frame_i in range(n_frames):
            particles = []
            for p in petals:
                y = p.y_at(frame_i)
                if 0 <= y <= CANVAS_H:
                    particles.append((int(p.x_at(frame_i)), int(y), p.color, p.size))

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
            img = self._draw_particles(img, particles)
            frames.append(img)
        return frames

    def _draw_particles(self, img: Image.Image, particles: list) -> Image.Image:
        img = img.copy()
        pixels = img.load()
        for x, y, color, size in particles:
            c = self._hex_to_rgb(color)
            for dx in range(size):
                for dy in range(size):
                    px, py = x + dx, y + dy
                    if 0 <= px < CANVAS_W and 0 <= py < CANVAS_H:
                        pixels[px, py] = c + (255,)
        return img

    def _hex_to_rgb(self, h: str) -> tuple:
        h = h.lstrip("#")
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))