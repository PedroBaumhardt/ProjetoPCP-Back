from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from app.core.config.current_adapters import token_adapter
from app.core.views.ErrorView import ErrorView

class JWTMiddleware(BaseHTTPMiddleware):
    _EXEMPT_ROUTES = [
        "/auth/login",
        "/auth/signin"
    ]

    def _get_token_from_header(self, request: Request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        return auth_header.split(" ")[1]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self._EXEMPT_ROUTES:
            return await call_next(request)

        token = self._get_token_from_header(request)
        if not token:
            return ErrorView(
                message="Token de autenticacao ausente ou invalido",
                status_code=401
            ).to_response()

        try:
            adapter = token_adapter()
            user = adapter.decode(token)
            
            request.state.user = user
            
        except jwt.ExpiredSignatureError:
            return ErrorView(
                message="Token expirado",
                status_code=401
            ).to_response()
        except (jwt.InvalidTokenError, Exception):
            return ErrorView(
                message="Token invalido",
                status_code=401
            ).to_response()

        return await call_next(request)
