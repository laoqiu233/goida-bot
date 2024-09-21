import asyncio
import pathlib

from common.storage import ArticlesStorage


class LocalArticlesStorage(ArticlesStorage):
    def __init__(self, path_prefix: str):
        self._path_prefix = path_prefix

        folder_path = pathlib.Path(self._path_prefix)

        if folder_path.exists and not folder_path.is_dir:
            raise ValueError(f"{folder_path} is not a directory")

    def _get_path(self, key: str):
        return f"{self._path_prefix}/{key}.pdf"

    def _blocking_store(self, key: str, content: bytes) -> None:
        path = pathlib.Path(self._get_path(key))
        path.parent.mkdir(exist_ok=True, parents=True)

        with open(path, "wb") as file:
            file.write(content)

    async def store(self, key: str, content: bytes) -> None:
        await asyncio.to_thread(self._blocking_store, key, content)

    def _blocking_read(self, key: str) -> bytes | None:
        with open(self._get_path(key), "rb") as file:
            return file.read()

    async def read(self, key: str) -> bytes | None:
        if not await self.exists(key):
            return None

        return await asyncio.to_thread(self._blocking_read, key)

    def _blocking_exists(self, key: str) -> bool:
        path = pathlib.Path(self._get_path(key))
        return path.exists()

    async def exists(self, key: str) -> bool:
        return await asyncio.to_thread(self._blocking_exists, key)
