from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.PedidoModel import PedidoModel
from app.core.repository.BaseRepository import BaseRepository


class PedidoRepository(BaseRepository[PedidoModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PedidoModel)
