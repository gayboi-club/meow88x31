from abc import ABC, abstractmethod
from PIL import Image


class Animation(ABC):
    name: str = "base"

    @abstractmethod
    def generate(self, badge) -> list[Image.Image]:
        pass
