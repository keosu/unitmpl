"""
应用配置管理
支持从环境变量和.env文件读取配置
"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    app_name: str = "法律咨询应用 API"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 数据库配置
    database_url: str = Field(
        default="postgresql://postgres:password@localhost:5432/lawchat_db",
        description="数据库连接URL"
    )
    database_echo: bool = False  # 是否打印SQL语句
    
    # Redis配置
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis连接URL"
    )
    
    # JWT认证配置
    secret_key: str = Field(
        default="your-super-secret-key-change-in-production",
        description="JWT密钥"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # 安全配置
    bcrypt_rounds: int = 12
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "https://your-frontend-domain.com"
    ]
    
    # 文件上传配置
    upload_max_size: int = 10 * 1024 * 1024  # 10MB
    upload_allowed_extensions: list[str] = [
        ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx"
    ]
    upload_path: str = "./uploads"
    
    # 邮件配置
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: Optional[str] = None
    
    # 第三方服务配置
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # 分页配置
    default_page_size: int = 20
    max_page_size: int = 100
    
    # 缓存配置
    cache_ttl: int = 3600  # 1小时
    
    # 日志配置
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 创建全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例，用于依赖注入"""
    return settings