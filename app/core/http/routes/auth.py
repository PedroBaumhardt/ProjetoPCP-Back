from typing import Awaitable, Callable

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.http.dependencies import SessionDep
from app.core.views.ErrorView import ErrorView
from app.core.views.BaseView import BaseView
from app.core.views.SuccessView import SuccessView
from app.core.controller.AuthController import AuthController
from app.core.schema.AuthSchema import AuthRequest

subrouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

async def _run(session: AsyncSession, action: Callable, success_message: str = "", **kwargs) -> BaseView:
    try:
        response = await action(**kwargs)
    # -- antes do ValueError: ValidationError herda dele
    except ValidationError as e:
        await session.rollback()
        return ErrorView(message="Erro na validacao",
                         errors=e.errors(include_url=False,
                                          include_context=False,
                                          include_input=False), status_code=422)
    except ValueError as e:
        await session.rollback()
        return ErrorView(message=str(e))
    except Exception as e:
        await session.rollback()
        return ErrorView(message=str(e))

    return SuccessView(message=success_message, **response)

@subrouter.post("/login")
async def login(session: SessionDep, body: AuthRequest):
    view = await _run(
        session=session,
        action=AuthController(session).login,
        email=body.email,
        password=body.password,
        success_message="Login bem sucedido"
    )
    return view.to_response()

@subrouter.post("/signin")
async def signin(session: SessionDep, body: AuthRequest):
    view = await _run(
        session=session,
        action=AuthController(session).register,
        email=body.email,
        password=body.password,
        success_message="Cadastro bem sucedido"
    )
    return view.to_response()