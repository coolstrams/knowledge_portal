from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv


class Settings(BaseSettings):
    # 应用基础配置
    app_name: str = "知识门户"
    app_version: str = "1.0.0"
    debug: bool = False

    # 数据库配置
    database_url: str = "mysql+pymysql://user:password@localhost/knowledge_portal"
    database_echo: bool = False

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    KB_SEARCH_URL: str = "http://127.0.0.1:8080/search"

    # JWT配置
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS配置
    allowed_origins: list = ["*"]
    allowed_methods: list = ["*"]
    allowed_headers: list = ["*"]

    # 文件上传配置
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: list = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx", ".txt"]

    # 分页配置
    default_page_size: int = 20
    max_page_size: int = 100

    # 搜索配置
    search_results_limit: int = 50

    # 缓存配置
    cache_ttl: int = 3600  # 1小时

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

VLLM_BASE_URL = "http://localhost:8000/v1"
VLLM_MODEL = "Qwen2.5-72B-Instruct"

REDIS_URL = "redis://localhost:6379/0"
REDIS_TTL = 60 * 60 * 24

load_dotenv()

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

KB_SEARCH_URL = settings.KB_SEARCH_URL
