import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.model.EstruturaProdutoModel import EstruturaProdutoModel
from app.core.repository.BaseRepository import BaseRepository


class EstruturaProdutoRepository(BaseRepository[EstruturaProdutoModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, EstruturaProdutoModel)

    async def get_by_product_id(self, product_id: uuid.UUID | str) -> EstruturaProdutoModel | None:
        if isinstance(product_id, str):
            product_id = uuid.UUID(product_id)
        qry = (
            select(EstruturaProdutoModel)
            .where(EstruturaProdutoModel.produto_id == product_id)
            .options(selectinload(EstruturaProdutoModel.componentes))
        )
        result = await self.session.execute(qry)
        return result.scalars().one_or_none()
