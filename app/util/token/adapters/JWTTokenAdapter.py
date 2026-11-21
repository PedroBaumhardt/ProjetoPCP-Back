from datetime import datetime, timedelta, UTC

import jwt

from app.core.config.Settings import Settings
from app.util.token.TokenPort import TokenPort
from app.core.model.UserModel import UserModel

class JWTTokenAdapter(TokenPort):

    _ALGO: str = "HS256"
    _EXPIRATION_TIME: timedelta = timedelta(hours=1)

    def __init__(self):
        settings = Settings.get_instance()
        self._secret = settings.JWT_SECRET

    def _build_payload(self, user: UserModel) -> dict:
        now = datetime.now(UTC)
        name = user.email.split("@")[0]

        payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,
            "name": name,
            "exp": now + self._EXPIRATION_TIME,
            "iat": now,
        }
        return payload

    def encode(self, user) -> str:
        return jwt.encode(
            self._build_payload(user),
            self._secret,
            algorithm=self._ALGO
        )

    def decode(self, token: str) -> UserModel:
        decoded = jwt.decode(
            token,
            self._secret,
            algorithms=[self._ALGO]
        )
        return UserModel(
            id=decoded["sub"],
            email=decoded["email"],
            role=decoded["role"],
        )