from fastapi import APIRouter

from app.core.controller.OrderController import OrderController
from app.core.http.dependencies import SessionDep
from app.core.schema.PrioritySchema import PrioritySchema
from app.core.views.SuccessView import SuccessView
from app.core.views.ErrorView import ErrorView
from app.core.views.TableView import TableView

subrouter = APIRouter(
    prefix="/order",
    tags=["order"]
)

@subrouter.get("/all")
async def get_all_order(session: SessionDep):
    try:
        tbl = await OrderController(session).get_all()
    except Exception as e:
        return ErrorView(message=str(e))
    return TableView(data=tbl, message="Pedidos carregados com sucesso")

@subrouter.get("/{id}")
async def get_order_by_id(session: SessionDep, id: str):
    try:
        ord = await OrderController(session).get_by_id(id)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Pedido carregado com sucesso", data=ord)

# POST

@subrouter.post("/")
async def create_order(session: SessionDep, body: OrderSchema): ...

# PUT

@subrouter.put("/{id}/priority")
async def update_order_priority(session: SessionDep, id: str, body: PrioritySchema): ...