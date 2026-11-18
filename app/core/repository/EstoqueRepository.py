from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.EstoqueModel import EstoqueModel
from app.core.repository.BaseRepository import BaseRepository


class EstoqueRepository(BaseRepository[EstoqueModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, EstoqueModel)
