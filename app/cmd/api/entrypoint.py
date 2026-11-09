from fastapi import FastAPI
from app.core.http.Router import Router

# Iniciando o APP e registrando as rotas
app = FastAPI()
router = Router()
router.register_to_app(app)