from PIL import Image, ImageDraw, ImageFont

from ..utils.colors import parse_color, make_gradient
from ..utils.fonts import load_font
from ..flags.palettes import get_flag
from .text import draw_centered_text, calc_auto_font_size


CANVAS_W = 88
CANVAS_H = 31


def render_frame(
    text: str,
    style,
    fg_color: str | tuple = "white",
    bg_type: str = "solid",
    bg_color: str | tuple = "#336699",
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
    anim_modifier=None,
) -> Image.Image:
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    fg = parse_color(fg_color) if isinstance(fg_color, str) else fg_color

    if flag_name:
        flag_colors = get_flag(flag_name)
        bg_img = _render_flag_bg(CANVAS_W, CANVAS_H, flag_colors)
    elif bg_type == "gradient" and bg_gradient:
        cols = [parse_color(c) if isinstance(c, str) else c for c in bg_gradient]
        bg_img = make_gradient(CANVAS_W, CANVAS_H, cols, gradient_direction)
    else:
        bc = parse_color(bg_color) if isinstance(bg_color, str) else bg_color
        bg_img = Image.new("RGBA", (CANVAS_W, CANVAS_H), bc + (255,))

    img.paste(bg_img, (0, 0))

    if gradient:
        grad_cols = [parse_color(c) if isinstance(c, str) else c for c in gradient]
        shared_grad_img = make_gradient(CANVAS_W, CANVAS_H, grad_cols, gradient_direction)
        img = _apply_gradient_border(img, shared_grad_img)
        fg_grad_for_text = grad_cols
    else:
        if border_gradient:
            border_cols = [parse_color(c) if isinstance(c, str) else c for c in border_gradient]
            border_grad_img = make_gradient(CANVAS_W, CANVAS_H, border_cols, gradient_direction)
            img = _apply_gradient_border(img, border_grad_img)
        elif border_color:
            img = style.apply_border(img, border_color)
        fg_grad_for_text = [parse_color(c) if isinstance(c, str) else c for c in fg_gradient] if fg_gradient else None

    if not font_size:
        font_size = calc_auto_font_size(text, font_path, font_weight=font_weight)
    draw = ImageDraw.Draw(img)
    font = load_font(font_path, font_size, weight=font_weight)

    display_text = text
    char_offset = 0
    particle_overlay = None
    extra_overlay = None

    if anim_modifier:
        display_text = anim_modifier.get("text", text)
        char_offset = anim_modifier.get("char_offset", 0)
        particle_overlay = anim_modifier.get("particles")
        extra_overlay = anim_modifier.get("overlay")

    tb_color = parse_color(text_border_color) if isinstance(text_border_color, str) else (text_border_color if text_border_color else None)
    draw_centered_text(draw, display_text, font, fg, CANVAS_W, CANVAS_H, y_offset=char_offset, border_color=tb_color, border_width=text_border_width, fg_gradient=fg_grad_for_text, img=img, gradient_direction=gradient_direction)

    if particle_overlay:
        for px, py, pcolor, psize in particle_overlay:
            c = parse_color(pcolor) if isinstance(pcolor, str) else pcolor
            for dx in range(psize):
                for dy in range(psize):
                    ix, iy = int(px + dx), int(py + dy)
                    if 0 <= ix < CANVAS_W and 0 <= iy < CANVAS_H:
                        img.putpixel((ix, iy), c + (255,))

    if extra_overlay:
        for x in range(CANVAS_W):
            for y in range(CANVAS_H):
                if 0 <= x < extra_overlay.width and 0 <= y < extra_overlay.height:
                    px = extra_overlay.getpixel((x, y))
                    if px[3] > 0:
                        img.putpixel((x, y), px)

    return img


def _apply_gradient_border(img: Image.Image, gradient: Image.Image, width: int = 2) -> Image.Image:
    out = img.copy()
    w, h = out.size
    for x in range(w):
        for row in range(width):
            if row < h:
                out.putpixel((x, row), gradient.getpixel((x, row)))
            if h - 1 - row >= 0:
                out.putpixel((x, h - 1 - row), gradient.getpixel((x, h - 1 - row)))
    for y in range(h):
        for col in range(width):
            if col < w:
                out.putpixel((col, y), gradient.getpixel((col, y)))
            if w - 1 - col >= 0:
                out.putpixel((w - 1 - col, y), gradient.getpixel((w - 1 - col, y)))
    return out


def _render_flag_bg(w: int, h: int, stripes: list) -> Image.Image:
    img = Image.new("RGBA", (w, h))
    n = len(stripes)

    if any(isinstance(s, dict) for s in stripes):
        y = 0
        for i, color_def in enumerate(stripes):
            if isinstance(color_def, dict):
                col = parse_color(color_def.get("color", "#000"))
                ratio = color_def.get("ratio", 1.0 / n)
                stripe_h = max(1, int(ratio * h))
            else:
                col = parse_color(color_def)
                remaining = n - i
                stripe_h = (h - y) // remaining
            if i == len(stripes) - 1:
                stripe_h = h - y
            for row in range(y, y + stripe_h):
                for x in range(w):
                    img.putpixel((x, row), col + (255,))
            y += stripe_h
    else:
        base = h // n
        rem = h % n
        start = (n - rem) // 2
        y = 0
        for i, color_def in enumerate(stripes):
            col = parse_color(color_def)
            size = base + (1 if start <= i < start + rem else 0)
            for row in range(y, y + size):
                for x in range(w):
                    img.putpixel((x, row), col + (255,))
            y += size
    return img