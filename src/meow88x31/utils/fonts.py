import os
import platform
from PIL import ImageFont


_DEFAULT_SIZE = 8


def find_default_font(size: int = _DEFAULT_SIZE):
    system = platform.system()
    candidates = []
    if system == "Windows":
        font_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
        candidates = [
            os.path.join(font_dir, "arial.ttf"),
            os.path.join(font_dir, "tahoma.ttf"),
            os.path.join(font_dir, "verdana.ttf"),
            os.path.join(font_dir, "segoeui.ttf"),
            os.path.join(font_dir, "lucon.ttf"),
            os.path.join(font_dir, "comic.ttf"),
            os.path.join(font_dir, "comici.ttf"),
            os.path.join(font_dir, "comicz.ttf"),
            os.path.join(font_dir, "cour.ttf"),
            os.path.join(font_dir, "consola.ttf"),
            os.path.join(font_dir, "segoepr.ttf"),
            os.path.join(font_dir, "segoesc.ttf"),
            os.path.join(font_dir, "gabriola.ttf"),
            os.path.join(font_dir, "framd.ttf"),
            os.path.join(font_dir, "impact.ttf"),
            os.path.join(font_dir, "georgia.ttf"),
            os.path.join(font_dir, "trebuc.ttf"),
            os.path.join(font_dir, "pala.ttf"),
            os.path.join(font_dir, "brush.ttf"),
            os.path.join(font_dir, "monotype.ttf"),
            os.path.join(font_dir, "terminal.ttf"),
        ]
    elif system == "Darwin":
        candidates = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Times.ttc",
            "/Library/Fonts/Arial.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def load_font(path: str | None, size: int = _DEFAULT_SIZE, weight: int = 400) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if path and os.path.exists(path):
        try:
            return ImageFont.truetype(path, size, weight=weight)
        except Exception:
            pass
    font = find_default_font(size)
    if weight > 400 and hasattr(font, "path"):
        try:
            return ImageFont.truetype(font.path, size, weight=weight)
        except Exception:
            pass
    return font


def list_system_fonts() -> list[str]:
    system = platform.system()
    fonts = []
    if system == "Windows":
        font_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    elif system == "Darwin":
        font_dir = "/System/Library/Fonts"
    else:
        font_dir = "/usr/share/fonts"
    if os.path.exists(font_dir):
        for f in os.listdir(font_dir):
            if f.lower().endswith((".ttf", ".otf", ".ttc")):
                fonts.append(os.path.join(font_dir, f))
    return sorted(fonts)
