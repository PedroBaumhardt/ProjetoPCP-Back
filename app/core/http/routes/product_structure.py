from fastapi import APIRouter

from app.core.controller.ProductStructureController import ProductStructureController
from app.core.http.dependencies import SessionDep
from app.core.views.SuccessView import SuccessView
from app.core.views.ErrorView import ErrorView
from app.core.views.TableView import TableView

subrouter = APIRouter(
    prefix="/product-structure",
    tags=["product-structure"]
)

@subrouter.get("/all")
async def get_all_product_structure(session: SessionDep):
    try:
        tbl = await ProductStructureController(session).get_all()
    except Exception as e:
        return ErrorView(message=str(e))
    return TableView(data=tbl, message="Estruturas de produtos carregadas com sucesso")

@subrouter.get("/{id}")
async def get_product_structure_by_id(session: SessionDep, id: str):
    try:
        ps = await ProductStructureController(session).get_by_id(id)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Estrutura de produto carregada com sucesso", data=ps)
