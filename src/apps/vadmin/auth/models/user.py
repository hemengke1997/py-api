from sqlalchemy import Column, String
from passlib.context import CryptContext
from src.db.db_base import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class VadminUser(BaseModel):
    __tablename__ = "vadmin_auth_user"
    __table_args__ = {"comment": "用户表"}

    telephone = Column(
        String(11), nullable=False, index=True, comment="手机号", unique=False
    )

    email = Column(String(50), index=True, nullable=False, comment="邮箱地址")

    password = Column(String(60), nullable=True, comment="密码")

    @staticmethod
    def verify_password(pwd: str, hashed_pwd: str) -> bool:
        return pwd_context.verify(pwd, hashed_pwd)

    @staticmethod
    def get_password_hash(pwd: str) -> str:
        return pwd_context.hash(pwd)
