import math
from PIL import Image, ImageDraw
from .base import Animation
from ..core.frame import render_frame, CANVAS_W, CANVAS_H
from ..core.text import calc_auto_font_size
from ..utils.fonts import load_font
from ..utils.colors import parse_color


class WaveAnimation(Animation):
    name = "wave"

    def generate(self, badge) -> list[Image.Image]:
        frames = []
        n_frames = 20
        font_size = badge.font_size if badge.font_size else calc_auto_font_size(badge.text, badge.font_path, font_weight=badge.font_weight)
        font = load_font(badge.font_path, font_size, weight=badge.font_weight)
        fg = parse_color(badge.fg_color)
        tb_color = parse_color(badge.text_border_color) if isinstance(badge.text_border_color, str) else (badge.text_border_color if badge.text_border_color else None)
        tb_width = badge.text_border_width

        def _char_border(d, cx, cy, ch):
            if tb_color:
                for dy in range(-tb_width, tb_width + 1):
                    for dx in range(-tb_width, tb_width + 1):
                        if dx == 0 and dy == 0:
                            continue
                        d.text((cx + dx, cy + dy), ch, font=font, fill=tb_color + (255,))
            d.text((cx, cy), ch, font=font, fill=fg + (255,))

        for frame_i in range(n_frames):
            img = render_frame(
                text="",
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
                font_size=font_size,
                font_weight=badge.font_weight,
                fg_gradient=badge.fg_gradient,
                border_gradient=badge.border_gradient,
                gradient=badge.gradient,
                gradient_direction=badge.gradient_direction,
            )
            draw = ImageDraw.Draw(img)
            text = badge.text
            total_w = 0
            char_sizes = []
            for ch in text:
                try:
                    bbox = font.getbbox(ch)
                    cw = bbox[2] - bbox[0]
                    ch_h = bbox[3] - bbox[1]
                except Exception:
                    cw, ch_h = 6, 8
                char_sizes.append((cw, ch_h))
                total_w += cw

            start_x = max(0, (CANVAS_W - total_w) // 2)
            base_y = CANVAS_H // 2

            x = start_x
            for j, ch in enumerate(text):
                cw, ch_h = char_sizes[j]
                offset = int(math.sin((frame_i / n_frames) * 6.28 + j * 1.0) * 3)
                y = base_y - ch_h // 2 + offset
                _char_border(draw, x, y, ch)
                x += cw
            frames.append(img)
        return frames
