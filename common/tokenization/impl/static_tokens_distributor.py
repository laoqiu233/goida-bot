from common.tokenization.tokens_distributor import TokensDistributor


class StaticTokensDistributor(TokensDistributor):
    """
    Staticly set owned set of tokens, useful only when there is a single instance
    with hard-coded tokens.
    """

    def __init__(self, total_tokens: int, my_tokens: set[int]):
        self._total_tokens = total_tokens
        self._my_tokens = my_tokens

    @classmethod
    def linear(cls, total_tokens: int, step: int = 1, offset: int = 0):
        return StaticTokensDistributor(
            total_tokens, set(range(offset, total_tokens, step))
        )

    async def tokens(self) -> set[int]:
        return self._my_tokens

    async def total_tokens(self) -> int:
        return self._total_tokens
