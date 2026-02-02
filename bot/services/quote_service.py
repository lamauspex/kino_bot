"""Сервис для работы с цитатами"""


from ..config.cache_config import CacheConfig
from ..interfaces import QuoteServiceProtocol


class QuoteService(QuoteServiceProtocol):

    def __init__(
        self,
        quote_repository,
        cache_config: CacheConfig = None
    ):
        self._config = cache_config
        self._quote_repository = quote_repository

    async def get_random(self) -> str:
        quote = await self._quote_repository.get_random()
        return f"...{quote.phrase}...\n{quote.author}"
