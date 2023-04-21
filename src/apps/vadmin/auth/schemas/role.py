from typing import Optional
from pydantic import BaseModel

from src.core.data_types import DatetimeStr


class Role(BaseModel):
    name: str
    disabled: bool = False
    order: Optional[int] = None
    desc: Optional[str] = None
    role_key: str
    is_admin: bool = False


class RoleSimpleOut(Role):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    class Config:
        orm_mode = True
