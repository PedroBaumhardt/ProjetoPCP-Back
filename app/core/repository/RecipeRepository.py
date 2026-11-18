from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.RecipeModel import RecipeModel
from app.core.repository.BaseRepository import BaseRepository


class RecipeRepository(BaseRepository[RecipeModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RecipeModel)
