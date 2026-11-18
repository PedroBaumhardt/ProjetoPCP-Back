from fastapi import APIRouter

subrouter = APIRouter(
    prefix="/import",
    tags=["import"]
)

@subrouter.get("/json")
async def import_json(): ...