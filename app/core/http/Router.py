from fastapi import APIRouter, FastAPI

from app.core.http.routes import example

DEFAULT_ROUTES: list[APIRouter] = [
    example.subrouter
]

class Router:

    def __init__(self):
        self._router = APIRouter()
        self._include_routes()

    def _include_routes(self) -> None:
        """
        Inicia as rotas dentro do roteador, usando como base a lista
        constante DEFAULT_ROUTES
        :return:
        """
        for route in DEFAULT_ROUTES:
            self._router.include_router(route)

    def register_to_app(self, app: FastAPI) -> None:
        """
        Registra as rotas do roteador no app fornecido
        :param app: App para registrar rotas
        :return:
        """
        app.include_router(self._router)