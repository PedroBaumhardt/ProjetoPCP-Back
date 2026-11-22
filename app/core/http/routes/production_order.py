from fastapi import APIRouter

from app.core.controller.ProductionOrderController import ProductionOrderController
from app.core.http.dependencies import SessionDep
from app.core.views.SuccessView import SuccessView
from app.core.views.ErrorView import ErrorView
from app.core.views.TableView import TableView

subrouter = APIRouter(
    prefix="/production-order",
    tags=["production-order"]
)

@subrouter.get("/all")
async def get_all_production_order(session: SessionDep):
    try:
        tbl = await ProductionOrderController(session).get_all()
    except Exception as e:
        return ErrorView(message=str(e))
    return TableView(data=tbl, message="Ordens de producao carregadas com sucesso")

@subrouter.get("/{id}")
async def get_production_order_by_id(session: SessionDep, id: str):
    try:
        po = await ProductionOrderController(session).get_by_id(id)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Ordem de producao carregada com sucesso", data=po)