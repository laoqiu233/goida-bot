from abc import ABC, abstractmethod


class ArticlesRenderer(ABC):
    @abstractmethod
    async def render(self, url: str) -> bytes | None:
        pass
