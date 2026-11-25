import uuid
from typing import TypeVar, Generic, Sequence

from app.core.model.BaseModel import BaseModel
from app.core.repository.BaseRepository import BaseRepository

ModelType = TypeVar("ModelType", bound=BaseModel)


# -- service base com operacoes padrao delegando ao repository
class BaseService(Generic[ModelType]):
    def __init__(self, repository: BaseRepository[ModelType]) -> None:
        self.repository = repository