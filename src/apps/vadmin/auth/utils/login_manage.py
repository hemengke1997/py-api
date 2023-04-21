from .. import models
from .validation.login import LoginForm, LoginResult


class LoginManage:
    """
    登录认证工具
    """

    async def password_login(
        self, data: LoginForm, user: models.VadminUser, **kwargs
    ) -> LoginResult:
        """
        验证用户密码
        """
        result = models.VadminUser.verify_password(data.password, user.password)
        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="手机号或密码错误")
