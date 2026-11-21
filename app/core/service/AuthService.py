from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.service.BaseService import BaseService
from app.core.repository.UserRepository import UserRepository
from app.core.model.UserModel import UserModel
from app.util.token.TokenPort import TokenPort
from app.core.config.current_adapters import token_adapter

class AuthService(BaseService[UserModel]):
    _phash: PasswordHash = PasswordHash.recommended()
    token_adapter: TokenPort
    repository: UserRepository

    def __init__(self, session: AsyncSession):
        super().__init__(UserRepository(session))
        self.token_adapter = token_adapter()


    async def _build_token(self, user: UserModel) -> str:
        return self.token_adapter.encode(user)

    async def login(self, email: str, password: str) -> str:
        usr = await self.repository.get_by_email(email)

        if usr is None:
            raise ValueError("User not found")

        pass_is_correct = self._phash.verify(password, usr.hashpw)
        if not pass_is_correct:
            raise ValueError("Invalid password")

        return await self._build_token(usr)

    async def register(self, email: str, password: str) -> str:
        usr = await self.repository.get_by_email(email)

        if usr is not None:
            raise ValueError("User already exists")

        hashpw = self._phash.hash(password)
        new_user = UserModel(email=email, hashpw=hashpw)
        await self.repository.create(new_user)

        return await self._build_token(new_user)