import importlib
import pkgutil
from .base import Style

__all__ = ["Style"]


def _import_builtins():
    __import__("meow88x31.styles.classic")
    __import__("meow88x31.styles.raised")
    __import__("meow88x31.styles.flat")
    __import__("meow88x31.styles.double")
    __import__("meow88x31.styles.groove")
    __import__("meow88x31.styles.none")


def discover_styles() -> dict[str, type[Style]]:
    _import_builtins()
    styles = {}
    for cls in Style.__subclasses__():
        try:
            inst = cls()
            styles[inst.name] = cls
        except Exception:
            pass
    try:
        eps = importlib.metadata.entry_points(group="meow88x31.styles")
        for ep in eps:
            try:
                cls = ep.load()
                inst = cls()
                styles[inst.name] = cls
            except Exception:
                pass
    except Exception:
        pass
    return styles


def get_style_names() -> list[str]:
    return sorted(discover_styles().keys())


def get_style(name: str) -> Style:
    styles = discover_styles()
    if name not in styles:
        raise ValueError(f"Unknown style: {name}. Available: {', '.join(styles)}")
    return styles[name]()
