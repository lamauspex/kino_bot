"""Сервис для работы с цитатами"""


from ..config import ServiceConfig
from ..interfaces import QuoteServiceProtocol


class QuoteService(QuoteServiceProtocol):

    def __init__(
        self,
        quote_repository,
        service_config: ServiceConfig = None
    ):
        self._config = service_config or ServiceConfig()
        self._quote_repository = quote_repository

    async def get_random(self) -> str:
        quote = await self._quote_repository.get_random()
        return f"...{quote.phrase}...\n{quote.author}"
