from fastapi import APIRouter

from app.core.controller.ProductController import ProductController
from app.core.http.dependencies import SessionDep
from app.core.views.SuccessView import SuccessView
from app.core.views.ErrorView import ErrorView
from app.core.views.TableView import TableView

subrouter = APIRouter(
    prefix="/product",
    tags=["product"]
)

@subrouter.get("/all")
async def get_all_product(session: SessionDep):
    try:
        tbl = await ProductController(session).get_all()
    except Exception as e:
        return ErrorView(message=str(e))
    return TableView(data=tbl, message="Produtos carregados com sucesso")

@subrouter.get("/{id}")
async def get_product_by_id(session: SessionDep, id: str):
    try:
        prod = await ProductController(session).get_by_id(id)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Produto carregado com sucesso", data=prod)
