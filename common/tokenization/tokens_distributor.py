import asyncio
from abc import ABC, abstractmethod
from logging import getLogger

logger = getLogger(__name__)

class TokensDistributor(ABC):
    """
    Manages tokens distributed across multiple instances.
    Tokens are integers ranging from 0 to total_tokens.

    Each instance can hold its own set of tokens, the distribution
    mechanic is left to implementations of this interface.

    A fair distribution is reached when all instances hold disjoint sets
    of tokens, where the difference between the number of tokens held by the
    richest and poorest instances is no more than 1.
    """

    @abstractmethod
    async def tokens(self) -> set[int]:
        """
        Tokens currently held by this instance.
        """

    @abstractmethod
    async def total_tokens(self) -> int:
        """
        Total number of tokens that are distributed.
        """

    async def generate_tokens(self, delay_seconds: float):
        """
        Creates an infinite stream of tokens that were distributed to this instance.
        Should serve as an entry point to a pipeline.

        Params:
        - delay_seconds: float - how many seconds to delay after each token sent
        """

        i = 0
        total_tokens = await self.total_tokens()

        while True:
            my_tokens = await self.tokens()

            if i in my_tokens:
                yield i
                logger.debug(f"Finished token {i}, sleeping for {delay_seconds} seconds")
                await asyncio.sleep(delay_seconds)

            i = (i + 1) % total_tokens
