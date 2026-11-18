from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.ProductionOrderModel import ProductionOrderModel
from app.core.repository.BaseRepository import BaseRepository


class ProductionOrderRepository(BaseRepository[ProductionOrderModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProductionOrderModel)
