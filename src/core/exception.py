# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/19 15:47
# @File           : exception.py
# @IDE            : PyCharm
# @desc           : 全局异常处理

from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from src.core.logger import logger


class CustomException(Exception):
    def __init__(
        self,
        msg: str,
        code: int = status.HTTP_400_BAD_REQUEST,
        status_code: int = status.HTTP_200_OK,
    ):
        self.msg = msg
        self.code = code
        self.status_code = status_code


def register_exception(app: FastAPI):
    """
    异常捕捉
    """

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        """
        自定义异常
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.msg, "code": exc.code},
        )

    @app.exception_handler(StarletteHTTPException)
    async def unicorn_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        重写HTTPException异常处理器
        """
        print("捕捉到重写HTTPException异常异常：unicorn_exception_handler")
        logger.error(exc.detail)
        print(exc.detail)
        return JSONResponse(
            status_code=200,
            content={
                "code": status.HTTP_400_BAD_REQUEST,
                "message": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        重写请求验证异常处理器
        """
        print("捕捉到重写请求验证异常异常：validation_exception_handler")
        logger.error(exc.errors())
        print(exc.errors())
        msg = exc.errors()[0].get("msg")
        if msg == "field required":
            msg = "请求失败，缺少必填项！"
        elif msg == "value is not a valid list":
            print(exc.errors())
            msg = f"类型错误，提交参数应该为列表！"
        elif msg == "value is not a valid int":
            msg = f"类型错误，提交参数应该为整数！"
        elif msg == "value could not be parsed to a boolean":
            msg = f"类型错误，提交参数应该为布尔值！"
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {"message": msg, "body": exc.body, "code": status.HTTP_400_BAD_REQUEST}
            ),
        )

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError):
        """
        捕获值异常
        """
        print("捕捉到值异常：value_exception_handler")
        logger.error(exc.__str__())
        print(exc.__str__())
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {"message": exc.__str__(), "code": status.HTTP_400_BAD_REQUEST}
            ),
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        捕获全部异常
        """
        print("捕捉到全局异常：all_exception_handler")
        logger.error(exc.__str__())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                {"message": "接口异常！", "code": status.HTTP_500_INTERNAL_SERVER_ERROR}
            ),
        )