from io import BytesIO
from uuid import UUID

from pgpt_python.client import AsyncPrivateGPTApi

from common.models.articles import DocumentChunk


class EmbeddingService:
    def __init__(self, pgpt: AsyncPrivateGPTApi):
        self._pgpt = pgpt

    async def embed(
        self, article_id: UUID, file_key: str, content: bytes
    ) -> list[DocumentChunk]:
        file = BytesIO(content)
        file.name = f"{file_key}.pdf"

        result = await self._pgpt.ingestion.ingest_file(file=file)
        chunks = [
            DocumentChunk(id=document.doc_id, article_id=article_id)
            for document in result.data
        ]

        return chunks
