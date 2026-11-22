from fastapi import APIRouter

from app.core.controller.StockController import StockController
from app.core.http.dependencies import SessionDep
from app.core.views.SuccessView import SuccessView
from app.core.views.ErrorView import ErrorView
from app.core.views.TableView import TableView

subrouter = APIRouter(
    prefix="/stock",
    tags=["stock"]
)

@subrouter.get("/all")
async def get_all_stock(session: SessionDep):
    try:
        tbl = await StockController(session).get_all()
    except Exception as e:
        return ErrorView(message=str(e))
    return TableView(data=tbl, message="Estoques carregados com sucesso")

@subrouter.get("/{id}")
async def get_stock_by_id(session: SessionDep, id: str):
    try:
        stk = await StockController(session).get_by_id(id)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Estoque carregado com sucesso", data=stk)
