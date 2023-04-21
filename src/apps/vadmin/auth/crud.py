from src.core.validator import vali_telephone
from src.core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.vadmin.auth import models, schemas


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

    def __init__(self, db: AsyncSession):
        super(UserDal, self).__init__(
            db, models=models.VadminUser, schema=schemas.UserSimpleOut
        )
