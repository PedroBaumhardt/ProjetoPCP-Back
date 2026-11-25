from fastapi import APIRouter

from app.core.controller.ProductionOrderController import ProductionOrderController
from app.core.http.dependencies import SessionDep
from app.core.schema.SequenceNumberSchema import SequenceNumberSchema
from app.core.schema.PrioritySchema import PrioritySchema
from app.core.schema.ProductionOrderSchema import ProductionOrderSchema
from app.core.views.SuccessView import SuccessView
from app.core.views.ErrorView import ErrorView
from app.core.views.TableView import TableView

subrouter = APIRouter(
    prefix="/production-order",
    tags=["production-order"]
)

# GET ========================================================================================

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


# POST =======================================================================================

@subrouter.post("/")
async def create_production_order(session: SessionDep, body: ProductionOrderSchema):
    try:
        await ProductionOrderController(session).create(body)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Ordem de producao criada com sucesso")


# UPDATE =====================================================================================

@subrouter.put("/{id}/priority")
async def update_production_order_priority(session: SessionDep, id: str, body: PrioritySchema):
    priority = body.to_priority()
    try:
        await ProductionOrderController(session).update_priority(id, priority)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Prioridade da ordem de producao atualizada com sucesso")

@subrouter.put("/{id}/sequence-number")
async def update_production_order_sequence_number(session: SessionDep, id: str, body: SequenceNumberSchema): ...

@subrouter.put("/{id}/start")
async def start_production_order(session: SessionDep, id: str): ...

@subrouter.put("/{id}/cancel")
async def cancel_production_order(session: SessionDep, id: str): ...

@subrouter.put("/{id}/produce")
async def produce_production_order(session: SessionDep, id: str): ...