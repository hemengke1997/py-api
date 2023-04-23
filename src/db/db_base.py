from src.core.database import Model
from sqlalchemy import Column, DateTime, Integer, func, Boolean


class BaseModel(Model):
    """
    公共 ORM 模型，基表
    """

    __abstract__ = True

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        comment="主键ID",
        index=True,
        nullable=False,
    )
    create_datetime = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_datetime = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    delete_datetime = Column(DateTime, nullable=True, comment="删除时间")
    is_delete = Column(Boolean, default=False, comment="是否软删除")
