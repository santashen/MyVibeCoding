from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """应用配置"""

    # API配置
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "大噜农场展示系统"

    # 数据库配置
    DATABASE_URL: str = "postgresql://dalu:dalu_password@localhost/dalu_farm"

    # CORS配置 - 支持逗号分隔的字符串或列表
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # 认证开关
    REQUIRE_AUTH: bool = False

    # 数据库初始化配置
    AUTO_CREATE_TABLES: bool = True  # 开发环境自动创建表，生产环境设为 false

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
