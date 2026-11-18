from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.ComponenteModel import ComponenteModel
from app.core.repository.BaseRepository import BaseRepository


class ComponenteRepository(BaseRepository[ComponenteModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ComponenteModel)
