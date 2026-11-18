from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.StepModel import StepModel
from app.core.repository.BaseRepository import BaseRepository


class StepRepository(BaseRepository[StepModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, StepModel)
