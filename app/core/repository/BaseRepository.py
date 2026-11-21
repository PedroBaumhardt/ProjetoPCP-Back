import uuid
from abc import ABC
from typing import TypeVar, Generic, Type, Sequence, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.BaseModel import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(ABC, Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        self.session = session
        self.model = model

    async def get_all(self) -> Sequence[ModelType]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, entity_id: uuid.UUID) -> ModelType | None:
        return await self.session.get(self.model, entity_id)

    # -- busca registros cujo campo esta em uma lista de valores (ex.: codigos)
    async def get_by_field_in(self, field: str, values: Iterable) -> Sequence[ModelType]:
        values = list(values)
        if not values:
            return []
        column = getattr(self.model, field)
        result = await self.session.execute(select(self.model).where(column.in_(values)))
        return result.scalars().all()

    async def create_many(self, entities: Sequence[ModelType]) -> Sequence[ModelType]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def create(self, entity: ModelType) -> ModelType:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: ModelType) -> ModelType:
        merged = await self.session.merge(entity)
        await self.session.flush()
        await self.session.refresh(merged)
        return merged

    async def delete(self, entity: ModelType) -> None:
        await self.session.delete(entity)
        await self.session.flush()
