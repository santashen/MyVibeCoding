"""Alembic 运行时环境配置"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.db.base import Base

# 导入所有模型（用于 autogenerate 支持）
from app.models.crop import Crop
from app.models.animal import Animal
from app.models.flower import Flower
from app.models.yield_record import YieldRecord

# Alembic Config 对象
config = context.config

# 从 settings 获取数据库 URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 解释配置文件用于 Python 日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 添加模型的 MetaData 对象，用于 autogenerate 支持
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """在离线模式下运行迁移 - 生成 SQL 脚本"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在在线模式下运行迁移 - 直接连接数据库"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
