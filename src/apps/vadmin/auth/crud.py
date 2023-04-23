from typing import Any, Optional
from src.core.exception import CustomException
from src.core.validator import vali_telephone
from src.core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils import status
from src.apps.vadmin.auth import models, schemas
from src.application import settings


class UserDal(DalBase):
    import_headers = [
        {"label": "姓名", "field": "name", "required": True},
        {"label": "昵称", "field": "nickname", "required": False},
        {
            "label": "手机号",
            "field": "telephone",
            "required": True,
            "rules": [vali_telephone],
        },
        {"label": "性别", "field": "gender", "required": False},
    ]

    model: models.VadminUser

    def __init__(self, db: AsyncSession):
        super(UserDal, self).__init__(db, model=models.VadminUser, schema=schemas.UserSimpleOut)

    async def create_data(
        self, data: schemas.UserIn, v_options: Optional[list] = None, v_return_obj: bool = False, v_schema: Any = None
    ):
        unique = await self.get_data(telephone=data.telephone, v_return_none=True)

        if unique:
            raise CustomException("手机号已存在", code=status.HTTP_ERROR)
        password = data.telephone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
        data.password = self.model.get_password_hash(password)
        data.avatar = data.avatar if data.avatar else settings.DEFAULT_AVATAR

        obj = self.model(**data.dict(exclude={"role_ids"}))
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)
