from typing import Awaitable, Callable

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import ValidationError

from app.core.http.dependencies import SessionDep
from app.core.controller.ImportController import ImportController
from app.core.views.SuccessView import SuccessView
from app.core.views.BaseView import BaseView
from app.core.views.ErrorView import ErrorView

subrouter = APIRouter(
    prefix="/import",
    tags=["import"],
)


# -- le o arquivo enviado e traduz erros de validacao/dominio para http
async def _run(action: Callable, file: UploadFile) -> BaseView:
    try:
        count = await action(await file.read())
        content = {"imported": count}
    except ValidationError as e:
        return ErrorView(message=e.errors(include_url=False, include_context=False), status_code=422)
    except ValueError as e:
        return ErrorView(message=str(e))
    return SuccessView(message=f"Imported ${count} entries", **content)


@subrouter.post("/recursos")
async def import_recursos(session: SessionDep, file: UploadFile = File(...)):
    return await _run(ImportController(session).import_recursos, file)


@subrouter.post("/materiais")
async def import_materiais(session: SessionDep, file: UploadFile = File(...)):
    return await _run(ImportController(session).import_materiais, file)


@subrouter.post("/produtos")
async def import_produtos(session: SessionDep, file: UploadFile = File(...)):
    return await _run(ImportController(session).import_produtos, file)


@subrouter.post("/estrutura-produtos")
async def import_estruturas_produto(session: SessionDep, file: UploadFile = File(...)):
    return await _run(ImportController(session).import_estruturas_produto, file)


@subrouter.post("/estoque")
async def import_estoque(session: SessionDep, file: UploadFile = File(...)):
    return await _run(ImportController(session).import_estoque, file)


@subrouter.post("/pedidos")
async def import_pedidos(session: SessionDep, file: UploadFile = File(...)):
    return await _run(ImportController(session).import_pedidos, file)


@subrouter.post("/ordens-producao")
async def import_ordens_producao(session: SessionDep, file: UploadFile = File(...)):
    return await _run(ImportController(session).import_ordens_producao, file)
