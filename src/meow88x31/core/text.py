from PIL import Image, ImageDraw, ImageFont
from ..utils.fonts import load_font
from ..utils.colors import make_gradient


CANVAS_W = 88


def measure_text(text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont) -> tuple[int, int]:
    try:
        bbox = font.getbbox(text)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])
    except Exception:
        return (0, 0)


def calc_auto_font_size(
    text: str,
    font_path: str | None = None,
    font_weight: int = 400,
    max_width: int = CANVAS_W - 6,
    min_size: int = 4,
    max_size: int = 12,
) -> int:
    for size in range(max_size, min_size - 1, -1):
        font = load_font(font_path, size, weight=font_weight)
        tw, _ = measure_text(text, font)
        if tw <= max_width:
            return size
    return min_size


def _render_gradient_fill(
    img: Image.Image,
    x: int, y: int,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    gradient_colors: list[tuple[int, int, int]],
    canvas_w: int = 88,
    canvas_h: int = 31,
    direction: str = "horizontal",
):
    mask = Image.new("L", (canvas_w, canvas_h), 0)
    md = ImageDraw.Draw(mask)
    md.text((x, y), text, font=font, fill=255)
    grad = make_gradient(canvas_w, canvas_h, gradient_colors, direction)
    img.paste(grad, (0, 0), mask)


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fg_color: tuple[int, int, int],
    width: int = 88,
    height: int = 31,
    y_offset: int = 0,
    border_color: tuple[int, int, int] | None = None,
    border_width: int = 1,
    fg_gradient: list[tuple[int, int, int]] | None = None,
    img: Image.Image | None = None,
    gradient_direction: str = "horizontal",
    **kwargs,
):
    tw, th = measure_text(text, font)
    x = max(0, (width - tw) // 2)
    y = max(1, (height - th) // 2 + y_offset - 1)

    if border_color:
        for dy in range(-border_width, border_width + 1):
            for dx in range(-border_width, border_width + 1):
                if dx == 0 and dy == 0:
                    continue
                draw.text((x + dx, y + dy), text, font=font, fill=border_color + (255,))

    if fg_gradient and img is not None:
        _render_gradient_fill(img, x, y, text, font, fg_gradient, width, height, direction=gradient_direction)
    else:
        draw.text((x, y), text, font=font, fill=fg_color + (255,))