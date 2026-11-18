from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.OrderProductionOrdersModel import OrderProductionOrdersModel
from app.core.repository.BaseRepository import BaseRepository


class OrderProductionOrdersRepository(BaseRepository[OrderProductionOrdersModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OrderProductionOrdersModel)
