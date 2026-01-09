"""
数据库管理 CLI 工具

用法:
    python -m app.db.cli init-tables    # 创建所有表
    python -m app.db.cli drop-tables    # 删除所有表
    python -m app.db.cli reset-db       # 重置数据库（删除+重建）
    python -m app.db.cli seed           # 插入种子数据
    python -m app.db.cli reseed         # 清除并重新插入种子数据
    python -m app.db.cli init-all       # 初始化全部（表+种子数据）
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.init_db import init_db, drop_all_tables, recreate_all_tables
from app.db.seed import seed_all, clear_seed_data


def init_tables() -> None:
    """创建所有数据库表"""
    print("[CLI] 正在创建数据库表...")
    init_db()


def drop_tables() -> None:
    """删除所有数据库表"""
    print("[CLI] 正在删除所有表...")
    confirm = input("[CLI] 确认删除所有表? (yes/no): ")
    if confirm.lower() == "yes":
        drop_all_tables()
    else:
        print("[CLI] 操作已取消")


def reset_db() -> None:
    """重置数据库"""
    print("[CLI] 正在重置数据库...")
    confirm = input("[CLI] 确认重置数据库? (yes/no): ")
    if confirm.lower() == "yes":
        recreate_all_tables()
    else:
        print("[CLI] 操作已取消")


def seed() -> None:
    """插入种子数据"""
    print("[CLI] 正在插入种子数据...")
    db: Session = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()


def reseed() -> None:
    """清除并重新插入种子数据"""
    print("[CLI] 正在重置种子数据...")
    confirm = input("[CLI] 确认重置种子数据? (yes/no): ")
    if confirm.lower() == "yes":
        db: Session = SessionLocal()
        try:
            clear_seed_data(db)
            seed_all(db)
        finally:
            db.close()
    else:
        print("[CLI] 操作已取消")


def init_all() -> None:
    """初始化全部（表+种子数据）"""
    print("[CLI] 正在初始化数据库...")
    init_db()
    db: Session = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()


if __name__ == "__main__":
    commands = {
        "init-tables": init_tables,
        "drop-tables": drop_tables,
        "reset-db": reset_db,
        "seed": seed,
        "reseed": reseed,
        "init-all": init_all,
    }

    if len(sys.argv) < 2:
        print("可用命令:")
        for cmd in commands.keys():
            print(f"  {cmd}")
        sys.exit(1)

    command = sys.argv[1]
    if command in commands:
        commands[command]()
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
