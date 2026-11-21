import uuid
from typing import TypeVar, Generic, Sequence

from app.core.model.BaseModel import BaseModel
from app.core.repository.BaseRepository import BaseRepository

ModelType = TypeVar("ModelType", bound=BaseModel)


# -- service base com operacoes padrao delegando ao repository
class BaseService(Generic[ModelType]):
    def __init__(self, repository: BaseRepository[ModelType]) -> None:
        self.repository = repository

    async def get_all(self) -> Sequence[ModelType]:
        return await self.repository.get_all()

    async def get_by_id(self, entity_id: uuid.UUID) -> ModelType | None:
        return await self.repository.get_by_id(entity_id)

    async def create(self, entity: ModelType) -> ModelType:
        return await self.repository.create(entity)

    async def update(self, entity: ModelType) -> ModelType:
        return await self.repository.update(entity)

    async def delete(self, entity: ModelType) -> None:
        await self.repository.delete(entity)
