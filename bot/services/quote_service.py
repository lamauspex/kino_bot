"""Сервис для работы с цитатами"""


from bot.repositories.interfaces import QuoteRepositoryProtocol
from .interfaces import QuoteServiceProtocol


class QuoteService(QuoteServiceProtocol):

    def __init__(self, quote_repository: QuoteRepositoryProtocol):
        self._quote_repository = quote_repository

    async def get_random(self) -> str:
        quote = await self._quote_repository.get_random()
        return f"...{quote.phrase}...\n{quote.author}"
