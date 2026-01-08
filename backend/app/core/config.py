from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""

    # API配置
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "大噜农场展示系统"

    # 数据库配置
    DATABASE_URL: str = "postgresql://dalu:dalu_password@localhost/dalu_farm"

    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173"]

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # 认证开关
    REQUIRE_AUTH: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
