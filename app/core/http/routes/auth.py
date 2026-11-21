from typing import Awaitable, Callable

from fastapi import APIRouter, HTTPException

from app.core.http.dependencies import SessionDep
from app.core.views.ErrorView import ErrorView
from app.core.views.BaseView import BaseView
from app.core.views.SuccessView import SuccessView
from app.core.controller.AuthController import AuthController

subrouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

async def _run(action: Callable, success_message: str = "", **kwargs) -> BaseView:
    try:
        response = await action(**kwargs)
    except ValueError as e:
        return ErrorView(message=str(e))
    except Exception as e:
        return ErrorView(message=str(e))

    return SuccessView(message=success_message, **response)

@subrouter.post("/login")
async def login(session: SessionDep, email: str, password: str):
    view = await _run(
        action=AuthController(session).login,
        email=email,
        password=password,
        success_message="Login bem sucedido"
    )
    return view.to_response()

@subrouter.post("/signin")
async def signin(session: SessionDep, email: str, password: str):
    view = await _run(
        action=AuthController(session).register,
        email=email,
        password=password,
        success_message="Cadastro bem sucedido"
    )
    return view.to_response()