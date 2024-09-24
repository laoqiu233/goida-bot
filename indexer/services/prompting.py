from logging import getLogger

from pgpt_python.client import AsyncPrivateGPTApi
from pgpt_python.types import ContextFilter

from common.models.articles import DocumentChunk
from indexer.services.prompt_storage import PromptStorage

logger = getLogger(__name__)


class PromptingService:
    def __init__(self, pgpt: AsyncPrivateGPTApi, prompt_stroage: PromptStorage):
        self._pgpt = pgpt
        self._prompt_storage = prompt_stroage

    async def prompt_from_chunks(
        self, chunks: list[DocumentChunk], prompt: str
    ) -> str | None:
        context_filter = ContextFilter(docs_ids=[chunk.id for chunk in chunks])

        result = await self._pgpt.contextual_completions.prompt_completion(
            prompt=prompt, use_context=True, context_filter=context_filter
        )

        logger.debug("Got response from pgpt: %s", result)

        if len(result.choices) == 0:
            return None

        first_choice = result.choices[0]

        if first_choice.message is None:
            return None

        return (
            None
            if first_choice.message.content is None
            else first_choice.message.content.replace("\u0000", "")
        )

    async def summarize(self, chunks: list[DocumentChunk]):
        return await self.prompt_from_chunks(
            chunks, self._prompt_storage.summarize_prompt()
        )

    async def full_text(self, title: str, chunks: list[DocumentChunk]):
        return await self.prompt_from_chunks(
            chunks, self._prompt_storage.full_text_prompt(title)
        )
