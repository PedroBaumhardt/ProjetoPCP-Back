# -- rotas de importacao dos arquivos json (um endpoint por arquivo do layout)
# -- ordem: recursos, materiais, produtos, estrutura_produtos, estoque, pedidos, ordens_producao

from typing import Awaitable, Callable

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import ValidationError

from app.core.http.dependencies import SessionDep
from app.core.controller.ImportController import ImportController

subrouter = APIRouter(
    prefix="/import",
    tags=["import"],
)


# -- le o arquivo enviado e traduz erros de validacao/dominio para http
async def _run(action: Callable[[bytes], Awaitable[int]], file: UploadFile) -> dict:
    try:
        count = await action(await file.read())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False, include_context=False))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


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
