from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.OrderModel import OrderModel
from app.core.repository.BaseRepository import BaseRepository


class OrderRepository(BaseRepository[OrderModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OrderModel)
