from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.EstruturaProdutoModel import EstruturaProdutoModel
from app.core.repository.BaseRepository import BaseRepository


class EstruturaProdutoRepository(BaseRepository[EstruturaProdutoModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, EstruturaProdutoModel)
