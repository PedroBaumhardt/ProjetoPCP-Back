# -- rotas de importacao csv

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.http.dependencies import SessionDep
from app.core.controller.ImportController import ImportController

subrouter = APIRouter(
    prefix="/import",
    tags=["import"],
)


# -- 1. Recurso ---------------------------------------------------------------

@subrouter.post("/recursos")
async def import_recursos(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_recursos(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 2. Material --------------------------------------------------------------

@subrouter.post("/materiais")
async def import_materiais(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_materiais(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 3. Cliente ----------------------------------------------------------------

@subrouter.post("/clientes")
async def import_clientes(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_clientes(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 4. Produto ----------------------------------------------------------------

@subrouter.post("/produtos")
async def import_produtos(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_produtos(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 5. Estoque ----------------------------------------------------------------

@subrouter.post("/estoque")
async def import_estoque(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_estoque(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 6. Roteiro (cabecalho) ----------------------------------------------------

@subrouter.post("/roteiros")
async def import_roteiros(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_roteiros(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 7. Passo Roteiro ----------------------------------------------------------

@subrouter.post("/passos-roteiro")
async def import_passos_roteiro(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_passos_roteiro(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 8. Estrutura Produto (cabecalho) ------------------------------------------

@subrouter.post("/estruturas-produto")
async def import_estruturas_produto(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_estruturas_produto(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 9. Componente -------------------------------------------------------------

@subrouter.post("/componentes")
async def import_componentes(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_componentes(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 10. Pedido ----------------------------------------------------------------

@subrouter.post("/pedidos")
async def import_pedidos(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_pedidos(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}


# -- 11. Ordem de Producao ----------------------------------------------------

@subrouter.post("/ordens-producao")
async def import_ordens_producao(session: SessionDep, file: UploadFile = File(...)):
    controller = ImportController(session)
    try:
        count = await controller.import_ordens_producao(await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": count}
