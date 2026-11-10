from fastapi import APIRouter

subrouter = APIRouter(
    prefix="/example",
    tags=["example"]
)

@subrouter.get("/")
async def hello_world():
    return {"hello": "world"}