import uuid
from typing import TypeVar, Generic, Sequence

from app.core.model.BaseModel import BaseModel
from app.core.service.BaseService import BaseService

T = TypeVar("T", bound=BaseModel)


# -- controller base com operacoes padrao delegando ao service
class BaseController(Generic[T]):
    def __init__(self, service: BaseService[T]) -> None:
        self.service = service

    async def get_all(self) -> Sequence[T]:
        return await self.service.get_all()

    async def get_by_id(self, entity_id: uuid.UUID) -> T | None:
        return await self.service.get_by_id(entity_id)

    async def create(self, entity: T) -> T:
        return await self.service.create(entity)

    async def update(self, entity: T) -> T:
        return await self.service.update(entity)

    async def delete(self, entity: T) -> None:
        await self.service.delete(entity)
