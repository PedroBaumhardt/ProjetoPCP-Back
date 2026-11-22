from fastapi import APIRouter

from app.core.controller.ResourceController import ResourceController
from app.core.http.dependencies import SessionDep
from app.core.views.SuccessView import SuccessView
from app.core.views.ErrorView import ErrorView
from app.core.views.TableView import TableView

subrouter = APIRouter(
    prefix="/resource",
    tags=["resource"]
)

@subrouter.get("/all")
async def get_all_resource(session: SessionDep):
    try:
        tbl = await ResourceController(session).get_all()
    except Exception as e:
        return ErrorView(message=str(e))
    return TableView(data=tbl, message="Recursos carregados com sucesso")

@subrouter.get("/{id}")
async def get_resource_by_id(session: SessionDep, id: str):
    try:
        res = await ResourceController(session).get_by_id(id)
    except Exception as e:
        return ErrorView(message=str(e))
    return SuccessView(message="Recurso carregado com sucesso", data=res)
