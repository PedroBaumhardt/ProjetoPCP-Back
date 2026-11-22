from fastapi import APIRouter

from app.core.controller.MaterialController import MaterialController
from app.core.http.dependencies import SessionDep
from app.core.views.SuccessView import SuccessView
from app.core.views.ErrorView import ErrorView
from app.core.views.TableView import TableView

subrouter = APIRouter(
    prefix="/material",
    tags=["material"]
)

@subrouter.get("/all")
async def get_all_material(session: SessionDep):
    try:
        tbl = await MaterialController(session).get_all()
    except Exception as e:
        return ErrorView(message=str(e))
    return TableView(data=tbl, message="Materiais carregados com sucesso")

@subrouter.get("/{id}")
async def get_material_by_id(session: SessionDep, id: str):
    try:
        mat = await MaterialController(session).get_by_id(id)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Material carregado com sucesso", data=mat)
