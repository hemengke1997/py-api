from typing import Optional
from fastapi import Request
from pydantic import BaseModel, validator
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.validator import vali_telephone
from src.apps.vadmin.auth import crud, schemas


class LoginForm(BaseModel):
    telephone: str
    password: str
    method: str = "0"  # 认证方式，0：密码登录，1：短信登录，2：微信一键登录
    platform: str = "0"  # 登录平台，0：PC端管理系统，1：移动端管理系统

    # validators
    _normalize_telephone = validator("telephone", allow_reuse=True)(vali_telephone)


class LoginResult(BaseModel):
    status: Optional[bool] = False
    user: Optional[schemas.UserOut] = None
    msg: Optional[str] = None

    # class Config:
    #     arbitrary_types_allowed = True


class LoginValidation:
    def __init__(self, func):
        self.func = func

    async def __call__(
        self, data: LoginForm, db: AsyncSession, request: Request
    ) -> LoginResult:
        self.result = LoginResult()
        if data.platform not in ["0", "1"] or data.method not in ["0", "1"]:
            self.result.msg = "无效参数"
            return self.result

        # user = await crud.UserDal(db).get_data(telephone=)
