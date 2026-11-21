from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.database import get_session

# -- scope="function": commit/rollback rodam antes da resposta ser enviada
SessionDep = Annotated[AsyncSession, Depends(get_session, scope="function")]