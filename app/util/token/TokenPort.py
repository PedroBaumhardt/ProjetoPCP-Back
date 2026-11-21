from abc import ABC, abstractmethod
from app.core.model.UserModel import UserModel

class TokenPort(ABC):

    @abstractmethod
    def encode(self, user: UserModel) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> UserModel: ...