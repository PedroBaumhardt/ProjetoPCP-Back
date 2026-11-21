from sqlalchemy.ext.asyncio import AsyncSession

from app.core.controller.BaseController import BaseController
from app.core.schema.AuthSchema import AuthSchema
from app.core.service.AuthService import AuthService


class AuthController(BaseController[AuthService]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AuthService(session))

    # -- levanta pydantic.ValidationError se email ou senha forem invalidos
    @staticmethod
    def _parse(email: str, password: str) -> AuthSchema:
        return AuthSchema(email=email, password=password)

    async def login(self, email: str, password: str) -> dict:
        dados = self._parse(email, password)
        tkn = await self.service.login(dados)
        return {"token": tkn}

    async def register(self, email: str, password: str) -> dict:
        dados = self._parse(email, password)
        tkn = await self.service.register(dados)
        return {"token": tkn}