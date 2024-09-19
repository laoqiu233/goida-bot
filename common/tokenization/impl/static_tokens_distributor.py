from common.tokenization.tokens_distributor import TokensDistributor


class StaticTokensDistributor(TokensDistributor):
    """
    Staticly set owned set of tokens, useful only when there is a single instance
    with hard-coded tokens.
    """

    def __init__(self, total_tokens: int, my_tokens: set[int]):
        self._total_tokens = total_tokens
        self._my_tokens = my_tokens

    async def tokens(self) -> set[int]:
        return self._my_tokens

    async def total_tokens(self) -> int:
        return self._total_tokens
