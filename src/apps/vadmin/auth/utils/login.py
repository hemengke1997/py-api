from fastapi import APIRouter, Depends, Request, Body, Response

from src.core.database import db_getter
from .validation.login import LoginForm
from sqlalchemy.ext.asyncio import AsyncSession


app = APIRouter()


@app.post(
    "/login/",
)
async def login_for_access_token(
    request: Request,
    data: LoginForm,
    db: AsyncSession = Depends(db_getter),
):
    pass
    # try:
    #   if data.method == "0":
    # result =

    # except:
