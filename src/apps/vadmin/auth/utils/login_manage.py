from datetime import timedelta, datetime

import jwt
from src.application import settings
from .. import models
from .validation.login import LoginForm, LoginResult, LoginValidation


class LoginManage:
    """
    登录认证工具
    """

    @LoginValidation
    async def password_login(self, data: LoginForm, user: models.VadminUser, **kwargs) -> LoginResult:
        """
        验证用户密码
        """
        result = models.VadminUser.verify_password(data.password, user.password)

        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="手机号或密码错误")

    @staticmethod
    def create_token(payload: dict, expires: timedelta = None):
        if expires:
            expire = datetime.utcnow() + expires
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})

        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt
