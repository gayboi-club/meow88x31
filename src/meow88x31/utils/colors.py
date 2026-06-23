import colorsys
from PIL import Image


NAMED_COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203),
    "purple": (128, 0, 128),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "navy": (0, 0, 128),
    "teal": (0, 128, 128),
    "maroon": (128, 0, 0),
    "lime": (0, 255, 0),
    "silver": (192, 192, 192),
}


def parse_color(s: str) -> tuple[int, int, int]:
    s = s.strip().lower()
    if s in NAMED_COLORS:
        return NAMED_COLORS[s]
    if s.startswith("#"):
        s = s[1:]
        if len(s) == 3:
            s = "".join(c * 2 for c in s)
        if len(s) == 6:
            r = int(s[0:2], 16)
            g = int(s[2:4], 16)
            b = int(s[4:6], 16)
            return (r, g, b)
    raise ValueError(f"Unknown color: {s}")


def color_to_rgb(c) -> tuple[int, int, int]:
    if isinstance(c, str):
        return parse_color(c)
    if isinstance(c, (list, tuple)) and len(c) >= 3:
        return (int(c[0]), int(c[1]), int(c[2]))
    raise ValueError(f"Invalid color: {c}")


def lerp_color(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def horizontal_gradient(w: int, h: int, colors: list[tuple[int, int, int]]) -> Image.Image:
    img = Image.new("RGBA", (w, h))
    n = len(colors)
    if n == 1:
        img.paste(colors[0] + (255,), (0, 0, w, h))
        return img
    for x in range(w):
        t = x / (w - 1) if w > 1 else 0
        fi = t * (n - 1)
        i = int(fi)
        frac = fi - i
        if i >= n - 1:
            col = colors[-1]
        else:
            col = lerp_color(colors[i], colors[i + 1], frac)
        for y in range(h):
            img.putpixel((x, y), col + (255,))
    return img


def diagonal_gradient(w: int, h: int, colors: list[tuple[int, int, int]]) -> Image.Image:
    img = Image.new("RGBA", (w, h))
    n = len(colors)
    if n == 1:
        img.paste(colors[0] + (255,), (0, 0, w, h))
        return img
    denom = (w - 1) + (h - 1)
    for y in range(h):
        for x in range(w):
            t = (x + y) / denom if denom > 0 else 0
            fi = t * (n - 1)
            i = int(fi)
            frac = fi - i
            if i >= n - 1:
                col = colors[-1]
            else:
                col = lerp_color(colors[i], colors[i + 1], frac)
            img.putpixel((x, y), col + (255,))
    return img


def make_gradient(w: int, h: int, colors: list[tuple[int, int, int]], direction: str = "horizontal") -> Image.Image:
    if direction == "vertical":
        return vertical_gradient(w, h, colors)
    elif direction == "diagonal":
        return diagonal_gradient(w, h, colors)
    return horizontal_gradient(w, h, colors)


def vertical_gradient(w: int, h: int, colors: list[tuple[int, int, int]]) -> Image.Image:
    img = Image.new("RGBA", (w, h))
    n = len(colors)
    if n == 1:
        img.paste(colors[0] + (255,), (0, 0, w, h))
        return img
    for y in range(h):
        t = y / (h - 1) if h > 1 else 0
        fi = t * (n - 1)
        i = int(fi)
        frac = fi - i
        if i >= n - 1:
            col = colors[-1]
        else:
            col = lerp_color(colors[i], colors[i + 1], frac)
        for x in range(w):
            img.putpixel((x, y), col + (255,))
    return img


def lighten_color(color: tuple[int, int, int], factor: float = 0.5) -> tuple[int, int, int]:
    return (
        min(255, int(color[0] + (255 - color[0]) * factor)),
        min(255, int(color[1] + (255 - color[1]) * factor)),
        min(255, int(color[2] + (255 - color[2]) * factor)),
    )


def darken_color(color: tuple[int, int, int], factor: float = 0.5) -> tuple[int, int, int]:
    return (
        max(0, int(color[0] * (1 - factor))),
        max(0, int(color[1] * (1 - factor))),
        max(0, int(color[2] * (1 - factor))),
    )


def hsv_cycle(step: int, total: int, saturation: float = 1.0, value: float = 1.0) -> tuple[int, int, int]:
    h = (step / total) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, saturation, value)
    return (int(r * 255), int(g * 255), int(b * 255))
