from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.ProdutoModel import ProdutoModel
from app.core.repository.BaseRepository import BaseRepository


class ProdutoRepository(BaseRepository[ProdutoModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProdutoModel)
