from abc import ABC, abstractmethod
from typing import Optional


class ArticlesStorage(ABC):
    """
    Store and retrieve rendered PDFs of articles by their file key
    """

    @abstractmethod
    async def store(self, key: str, content: bytes) -> None:
        pass

    @abstractmethod
    async def read(self, key: str) -> Optional[bytes]:
        pass
