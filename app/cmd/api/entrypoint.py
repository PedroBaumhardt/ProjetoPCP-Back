from fastapi import FastAPI

from app.cmd.api.lifespan import lifespan
from app.core.http.Router import Router

# Iniciando o APP e registrando as rotas
app = FastAPI(
    lifespan=lifespan
)
router = Router()
router.register_to_app(app)