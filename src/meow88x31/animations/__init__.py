import importlib
from .base import Animation

__all__ = ["Animation"]


def _import_builtins():
    __import__("meow88x31.animations.typing")
    __import__("meow88x31.animations.blossom")
    __import__("meow88x31.animations.blink")
    __import__("meow88x31.animations.snow")
    __import__("meow88x31.animations.rainbow")
    __import__("meow88x31.animations.wave")
    __import__("meow88x31.animations.scanline")


def discover_animations() -> dict[str, type[Animation]]:
    _import_builtins()
    animations = {}
    for cls in Animation.__subclasses__():
        try:
            inst = cls()
            animations[inst.name] = cls
        except Exception:
            pass
    try:
        eps = importlib.metadata.entry_points(group="meow88x31.animations")
        for ep in eps:
            try:
                cls = ep.load()
                inst = cls()
                animations[inst.name] = cls
            except Exception:
                pass
    except Exception:
        pass
    return animations


def get_animation_names() -> list[str]:
    return sorted(discover_animations().keys())


def get_animation(name: str) -> Animation:
    animations = discover_animations()
    if name not in animations:
        raise ValueError(f"Unknown animation: {name}. Available: {', '.join(animations)}")
    return animations[name]()
