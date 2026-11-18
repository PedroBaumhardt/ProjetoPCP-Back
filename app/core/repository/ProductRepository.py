from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.ProductModel import ProductModel
from app.core.repository.BaseRepository import BaseRepository


class ProductRepository(BaseRepository[ProductModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProductModel)
