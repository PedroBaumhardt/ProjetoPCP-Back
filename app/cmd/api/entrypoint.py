from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.cmd.api.lifespan import lifespan
from app.core.http.Router import Router
from app.core.middleware.JWTMiddleware import JWTMiddleware
from app.core.views.ErrorView import ErrorView

# Iniciando o APP e registrando as rotas
app = FastAPI(
    lifespan=lifespan
)
app.add_middleware(JWTMiddleware)

router = Router()
router.register_to_app(app)


# -- erro de validacao do request (body/query/arquivo ausente ou invalido) no mesmo formato das outras respostas;
@app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    errors = [
        {key: error[key] for key in ("type", "loc", "msg") if key in error}
        for error in exc.errors()
    ]
    return ErrorView(message="Erro na validacao", errors=errors, status_code=422).to_response()
