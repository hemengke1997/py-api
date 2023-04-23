from datetime import timedelta
from fastapi import APIRouter, Depends, Request, Body, Response
from src.application import settings
from src.apps.vadmin.auth.utils.login_manage import LoginManage

from src.core.database import db_getter
from src.utils.response import ErrorResponse, SuccessResponse
from .validation.login import LoginForm
from sqlalchemy.ext.asyncio import AsyncSession


app = APIRouter()


@app.post(
    "/login/",
)
async def login_for_access_token(
    request: Request,
    data: LoginForm,
    manage: LoginManage = Depends(),
    db: AsyncSession = Depends(db_getter),
):
    try:
        if data.method == "0":
            print(data, request)
            result = await manage.password_login(data, db, request)
        else:
            raise ValueError("无效参数")

        if not result.status:
            raise ValueError(result.msg)

        access_token = LoginManage.create_token({"sub": result.user.telephone, "is_refresh": False})

        expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = LoginManage.create_token({"sub": result.user.telephone, "is_refresh": True}, expires=expires)
        resp = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "is_reset_password": result.user.is_reset_password,
            "is_wx_server_openid": result.user.is_wx_server_openid,
        }
        return SuccessResponse(resp)

    except ValueError as e:
        # await VadminLoginRecord.create_login_record(db, data, False, request, {"message": str(e)})
        return ErrorResponse(msg=str(e))
