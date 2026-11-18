from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.MaterialModel import MaterialModel
from app.core.repository.BaseRepository import BaseRepository


class MaterialRepository(BaseRepository[MaterialModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MaterialModel)
