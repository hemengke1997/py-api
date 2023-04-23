from typing import List, Optional
from pydantic import BaseModel
from src.core.data_types import DatetimeStr, Email, Telephone
from .role import RoleSimpleOut


class BaseUser(BaseModel):
    name: Optional[str] = None
    telephone: Telephone
    email: Optional[Email] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False
    gender: Optional[str] = "0"
    is_wx_server_openid: Optional[bool] = False


class UserIn(BaseUser):
    """
    创建用户
    """

    role_ids: Optional[List[int]] = []
    password: Optional[str] = ""


class UserSimpleOut(BaseUser):
    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr
    is_reset_password: Optional[bool] = None
    last_login: Optional[DatetimeStr] = None
    last_ip: Optional[str] = None

    class Config:
        orm_mode = True


class UserOut(UserSimpleOut):
    roles: Optional[List[RoleSimpleOut]] = []

    class Config:
        orm_mode = True
