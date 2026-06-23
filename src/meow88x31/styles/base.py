from abc import ABC, abstractmethod
from PIL import Image


class Style(ABC):
    name: str = "base"

    @abstractmethod
    def apply_border(self, image: Image.Image, border_color: str | tuple | None = None) -> Image.Image:
        pass
