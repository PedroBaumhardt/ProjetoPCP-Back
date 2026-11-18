from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.RecursoModel import RecursoModel
from app.core.repository.BaseRepository import BaseRepository


class RecursoRepository(BaseRepository[RecursoModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RecursoModel)
