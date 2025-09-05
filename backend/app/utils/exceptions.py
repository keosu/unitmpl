"""
自定义异常和异常处理器
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


class BaseCustomException(Exception):
    """自定义异常基类"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserNotFoundError(BaseCustomException):
    """用户不存在异常"""
    def __init__(self, user_id: str = None):
        message = f"用户不存在: {user_id}" if user_id else "用户不存在"
        super().__init__(message, 404)


class DuplicateUserError(BaseCustomException):
    """用户重复异常"""
    def __init__(self, field: str = "用户"):
        super().__init__(f"{field}已存在", 409)


class InvalidCredentialsError(BaseCustomException):
    """无效凭据异常"""
    def __init__(self):
        super().__init__("用户名或密码错误", 401)


class InsufficientPermissionError(BaseCustomException):
    """权限不足异常"""
    def __init__(self, action: str = "执行此操作"):
        super().__init__(f"没有权限{action}", 403)


def setup_exception_handlers(app: FastAPI):
    """设置全局异常处理器"""
    
    @app.exception_handler(BaseCustomException)
    async def custom_exception_handler(request: Request, exc: BaseCustomException):
        """自定义异常处理器"""
        logger.warning(f"自定义异常: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.message,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """HTTP异常处理器"""
        logger.warning(f"HTTP异常: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """数据库完整性错误处理器"""
        logger.error(f"数据库完整性错误: {str(exc)}")
        return JSONResponse(
            status_code=409,
            content={
                "error": True,
                "message": "数据冲突，可能是重复的记录",
                "status_code": 409
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """通用异常处理器"""
        logger.error(f"未处理的异常: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "服务器内部错误",
                "status_code": 500
            }
        )