import uuid
from typing import TypeVar, Generic, Sequence

from app.core.model.BaseModel import BaseModel
from app.core.repository.BaseRepository import BaseRepository

T = TypeVar("T", bound=BaseModel)


# -- service base com operacoes padrao delegando ao repository
class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]) -> None:
        self.repository = repository

    async def get_all(self) -> Sequence[T]:
        return await self.repository.get_all()

    async def get_by_id(self, entity_id: uuid.UUID) -> T | None:
        return await self.repository.get_by_id(entity_id)

    async def create(self, entity: T) -> T:
        return await self.repository.create(entity)

    async def update(self, entity: T) -> T:
        return await self.repository.update(entity)

    async def delete(self, entity: T) -> None:
        await self.repository.delete(entity)
