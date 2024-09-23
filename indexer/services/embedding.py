from io import BytesIO
from uuid import UUID

from pgpt_python.client import AsyncPrivateGPTApi

from common.models.articles import ChunkType, DocumentChunk


class EmbeddingService:
    def __init__(self, pgpt: AsyncPrivateGPTApi):
        self._pgpt = pgpt

    async def embed_file(
        self, article_id: UUID, file_key: str, content: bytes
    ) -> list[DocumentChunk]:
        file = BytesIO(content)
        file.name = f"{file_key}.pdf"

        result = await self._pgpt.ingestion.ingest_file(file=file)
        chunks = [
            DocumentChunk(
                id=document.doc_id, article_id=article_id, chunk_type=ChunkType.RAW
            )
            for document in result.data
        ]

        return chunks

    async def embed_full_text(
        self, article_id: UUID, file_key: str, full_text: str
    ) -> list[DocumentChunk]:
        return await self._embed_text(
            article_id, file_key, full_text, ChunkType.FULL_TEXT
        )

    async def embed_summary(
        self, article_id: UUID, file_key: str, summary: str
    ) -> list[DocumentChunk]:
        return await self._embed_text(article_id, file_key, summary, ChunkType.SUMMARY)

    async def _embed_text(
        self, article_id: UUID, file_key: str, text: str, chunk_type: ChunkType
    ):
        name = f"{file_key}_{chunk_type.name}"

        result = await self._pgpt.ingestion.ingest_text(file_name=name, text=text)
        chunks = [
            DocumentChunk(
                id=document.doc_id, article_id=article_id, chunk_type=chunk_type
            )
            for document in result.data
        ]

        return chunks
