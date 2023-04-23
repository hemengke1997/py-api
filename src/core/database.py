from sqlalchemy import MetaData
from src.application.settings import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_TYPE
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker


def create_async_engine_session(database_url: str, database_type: str = "mysql"):
    """
    创建数据库会话

    相关配置文档：https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
    创建异步引擎：https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine

    database_url  dialect+driver://username:password@host:port/database
    max_overflow 超过连接池大小外最多创建的连接
    pool_size=5,     # 连接池大小
    pool_timeout=20, # 池中没有连接最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）

    :param database_type: 数据库类型
    :param database_url: 数据库地址
    :return:
    """

    engine = create_async_engine(
        database_url,
        echo=True,
        pool_pre_ping=True,
        pool_recycle=3600,
        future=True,
        max_overflow=5,
        connect_args={"check_same_thread": False, "timeout": 30} if database_type == "sqlite3" else {},
    )
    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=True,
        class_=AsyncSession,
    )


class Base:
    """将表名改为小写"""

    @declared_attr
    def __tablename__(self):
        table_name = self.__tablename__
        if not table_name:
            model_name = self.__name__
            ls = []
            for index, char in enumerate(model_name):
                if char.isupper() and index != 0:
                    ls.append("_")
                ls.append(char)
            table_name = "".join(ls).lower()
        return table_name


"""
创建基本映射类
稍后，我们将继承该类，创建每个 ORM 模型
"""
Model = declarative_base(name="Model", cls=Base)

meta = MetaData()


async def db_getter():
    async with create_async_engine_session(SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_TYPE)() as session:
        async with session.begin():
            await session.run_sync(meta.create_all)
            yield session
