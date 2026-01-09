"""
数据库初始化模块
用于开发环境自动创建表结构
"""
from sqlalchemy import inspect
from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    """
    创建所有数据库表

    开发环境使用：只创建不存在的表，不修改已有表结构
    生产环境请使用 Alembic 迁移
    """
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    # 获取所有模型表名
    model_tables = Base.metadata.tables.keys()

    # 只创建不存在的表
    tables_to_create = [t for t in model_tables if t not in existing_tables]

    if tables_to_create:
        Base.metadata.create_all(bind=engine, tables=[Base.metadata.tables[t] for t in tables_to_create])
        print(f"[DB] 已创建表: {', '.join(tables_to_create)}")
    else:
        print("[DB] 所有表已存在，跳过创建")


def drop_all_tables() -> None:
    """
    删除所有表（谨慎使用！）

    仅用于开发环境重置数据库
    """
    Base.metadata.drop_all(bind=engine)
    print("[DB] 已删除所有表")


def recreate_all_tables() -> None:
    """
    重新创建所有表（谨慎使用！）

    仅用于开发环境重置数据库
    """
    drop_all_tables()
    Base.metadata.create_all(bind=engine)
    print("[DB] 已重新创建所有表")
