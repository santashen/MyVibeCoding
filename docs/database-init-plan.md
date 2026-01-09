# 大噜农场展示系统 - 数据库初始化方案

## 目标
创建数据库初始化机制，包括：
1. **开发环境自动建表** - 应用启动时自动创建不存在的表
2. **Alembic 迁移配置** - 生产环境数据库版本管理
3. **测试种子数据** - 每种类型 3-5 条测试数据

---

## 数据库结构回顾

### 数据表
| 表名 | 说明 | 主要字段 |
|------|------|----------|
| `crops` | 粮食作物 | name, variety, area, plant_date, status (growing/harvested/failed) |
| `animals` | 动物 | name, variety, quantity, product_type (milk/egg/wool/meat/honey/other) |
| `flowers` | 花卉 | name, variety, quantity, bloom_season, colors (JSON), purpose |
| `yield_records` | 产量记录 | crop_id (FK), record_date, quantity, unit, area_harvested |

### 枚举值

```python
# 粮食状态
CropStatus: growing, harvested, failed

# 粮食产量单位
CropUnit: ton, kg, gram

# 动物产品类型
ProductType: milk, egg, wool, meat, honey, other

# 花卉用途
FlowerPurpose: ornamental, sale, essential_oil, medicinal, other

# 开花季节
BloomSeason: spring, summer, autumn, winter, all_year, multiple
```

---

## 需要创建的文件

### 1. `backend/app/db/init_db.py`
**职责**: 自动建表逻辑，开发环境启动时调用

**核心函数**:
- `init_db()` - 创建所有不存在的表
- `drop_all_tables()` - 删除所有表（开发重置用）
- `recreate_all_tables()` - 重新创建所有表

### 2. `backend/app/db/seed.py`
**职责**: 提供测试种子数据

**种子数据内容**:
| 类型 | 数量 | 数据示例 |
|------|------|----------|
| 粮食 | 5条 | 水稻(已收获)、小麦(已收获)、玉米(生长中)、大豆(生长中)、红薯(失败) |
| 动物 | 5条 | 奶牛、蛋鸡、绵羊、蜜蜂、肉兔 |
| 花卉 | 5条 | 月季、薰衣草、牡丹、金银花、向日葵 |
| 产量记录 | 4条 | 关联水稻和小麦的收获记录 |

**核心函数**:
- `seed_crops(db)` - 插入粮食数据
- `seed_animals(db)` - 插入动物数据
- `seed_flowers(db)` - 插入花卉数据
- `seed_yield_records(db)` - 插入产量记录
- `seed_all(db)` - 插入所有种子数据
- `clear_seed_data(db)` - 清除种子数据

### 3. `backend/app/db/cli.py`
**职责**: 命令行管理工具

**可用命令**:
```bash
cd backend
python -m app.db.cli init-tables    # 创建表
python -m app.db.cli seed            # 插入种子数据
python -m app.db.cli init-all        # 初始化全部（表+种子数据）
python -m app.db.cli drop-tables     # 删除所有表
python -m app.db.cli reset-db        # 重置数据库
python -m app.db.cli reseed          # 重新插入种子数据
```

### 4. `backend/alembic.ini`
**职责**: Alembic 主配置文件

**关键配置**:
- 数据库连接 URL
- 迁移脚本位置 (`script_location = alembic`)
- Python 路径设置

### 5. `backend/alembic/env.py`
**职责**: Alembic 运行时环境配置

**关键内容**:
- 导入所有模型（用于 autogenerate）
- 配置数据库连接
- 定义在线/离线迁移模式

### 6. `backend/alembic/script.py.mako`
**职责**: 迁移脚本模板

**作用**: 定义生成迁移文件的格式

---

## 需要修改的文件

### 1. `backend/app/core/config.py`
**修改内容**: 添加环境变量控制

```python
# 数据库初始化配置
AUTO_CREATE_TABLES: bool = True  # 开发环境自动创建表，生产环境设为 false
```

### 2. `backend/app/main.py`
**修改内容**: 应用启动时自动建表

```python
from app.db.init_db import init_db

# 在 app = FastAPI(...) 之前添加
if settings.AUTO_CREATE_TABLES:
    init_db()
```

### 3. `.env.example`
**修改内容**: 添加环境变量说明

```bash
# 数据库初始化配置
AUTO_CREATE_TABLES=true    # 开发环境自动创建表，生产环境设为 false
```

---

## 使用流程

### 首次初始化（开发环境）
```bash
cd backend
python -m app.db.cli init-all
```

输出示例：
```
[DB] 已创建表: crops, animals, flowers, yield_records
[Seed] 开始初始化种子数据...
[Seed] 已创建 5 条粮食数据
[Seed] 已创建 5 条动物数据
[Seed] 已创建 5 条花卉数据
[Seed] 已创建 4 条产量记录
[Seed] 种子数据初始化完成
```

### 启动应用（自动建表）
设置 `AUTO_CREATE_TABLES=true` 后，启动应用会自动创建不存在的表：
```bash
uvicorn app.main:app --reload
```

### Alembic 迁移（生产环境）

```bash
cd backend

# 创建初始迁移
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head

# 后续模型变更后
alembic revision --autogenerate -m "Add new field"
alembic upgrade head

# 查看当前版本
alembic current

# 查看迁移历史
alembic history

# 回滚一个版本
alembic downgrade -1
```

### Docker 环境执行
```bash
# 在容器内执行初始化
docker-compose exec backend python -m app.db.cli init-all

# 或运行迁移
docker-compose exec backend alembic upgrade head
```

---

## 种子数据详细内容

### 粮食数据 (5条)
| 名称 | 品种 | 面积(亩) | 种植日期 | 预计收获 | 实际收获 | 产量 | 状态 |
|------|------|----------|----------|----------|----------|------|------|
| 水稻 | 杂交稻汕优63 | 15.5 | 2024-04-15 | 2024-09-20 | 2024-09-18 | 9300kg | harvested |
| 小麦 | 济麦22 | 22.0 | 2023-10-10 | 2024-06-05 | 2024-06-08 | 13200kg | harvested |
| 玉米 | 郑单958 | 18.0 | 2024-05-20 | 2024-09-30 | - | 0 | growing |
| 大豆 | 黑农84 | 8.5 | 2024-06-05 | 2024-10-15 | - | 0 | growing |
| 红薯 | 徐薯32 | 5.0 | 2024-03-20 | 2024-09-01 | - | 0 | failed |

### 动物数据 (5条)
| 名称 | 品种 | 数量 | 购入日期 | 产品类型 | 日产产量 | 单位 |
|------|------|------|----------|----------|----------|------|
| 奶牛 | 荷斯坦奶牛 | 12 | 2023-03-15 | milk | 280 | 升 |
| 蛋鸡 | 海兰褐 | 150 | 2024-01-10 | egg | 135 | 个 |
| 绵羊 | 美利奴羊 | 25 | 2023-06-20 | wool | 0 | 千克 |
| 蜜蜂 | 意大利蜂 | 30 | 2024-04-01 | honey | 2.5 | 千克 |
| 肉兔 | 新西兰兔 | 60 | 2024-02-15 | meat | 0 | 千克 |

### 花卉数据 (5条)
| 名称 | 品种 | 数量 | 种植日期 | 开花季节 | 颜色 | 用途 |
|------|------|------|----------|----------|------|------|
| 月季 | 和平月季 | 200 | 2023-11-05 | 多季 | 粉色/白色/黄色 | sale |
| 薰衣草 | 真薰衣草 | 500 | 2023-09-15 | 夏季 | 紫色 | essential_oil |
| 牡丹 | 洛阳红 | 80 | 2023-10-20 | 春季 | 红色/深红 | ornamental |
| 金银花 | 大毛花 | 300 | 2024-03-10 | 全年 | 白色/黄色 | medicinal |
| 向日葵 | 食用葵 | 1000 | 2024-04-20 | 夏季 | 黄色 | other |

---

## 架构流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                      应用启动                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │  AUTO_CREATE_TABLES=true?     │
              └───────────────────────────────┘
                     │Yes            │No
                     ▼               ▼
            ┌──────────────┐   ┌──────────────┐
            │  init_db()   │   │ 等待 Alembic │
            │ 自动创建表    │   │   迁移执行   │
            └──────────────┘   └──────────────┘
                     │
                     ▼
            ┌───────────────────────────────┐
            │  手动执行 CLI 或 API 写入     │
            │  python -m app.db.cli seed    │
            └───────────────────────────────┘
                     │
                     ▼
            ┌───────────────────────────────┐
            │        数据就绪               │
            └───────────────────────────────┘
```

---

## 文件结构总览

```
backend/
├── alembic.ini                          # Alembic 配置文件
├── alembic/
│   ├── env.py                           # 迁移运行时环境
│   ├── script.py.mako                   # 迁移脚本模板
│   └── versions/                        # 迁移版本目录
├── app/
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py                      # SQLAlchemy Base
│   │   ├── session.py                   # 数据库会话
│   │   ├── init_db.py                   # 新增：自动建表逻辑
│   │   ├── seed.py                      # 新增：种子数据
│   │   └── cli.py                       # 新增：CLI 工具
│   ├── core/
│   │   └── config.py                    # 修改：添加 AUTO_CREATE_TABLES
│   └── main.py                          # 修改：启动时调用 init_db()
```

---

## 开发建议

1. **本地开发**: 设置 `AUTO_CREATE_TABLES=true`，让应用自动创建表
2. **种子数据**: 使用 `python -m app.db.cli init-all` 快速初始化
3. **数据重置**: 使用 `python -m app.db.cli reseed` 重新加载种子数据
4. **生产部署**: 设置 `AUTO_CREATE_TABLES=false`，使用 Alembic 迁移
5. **数据安全**: 生产环境永远不要使用 `drop_tables` 或 `reset-db`

---

## 故障排查

### 问题: 表已存在错误
**解决**: `init_db()` 会自动跳过已存在的表，不会报错

### 问题: 种子数据重复插入
**解决**: `seed_*` 函数会检查数据是否已存在，自动跳过

### 问题: Alembic 无法检测模型变化
**解决**: 确保 `alembic/env.py` 中导入了所有模型

### 问题: 外键关联失败
**解决**: 确保先插入被引用的数据（如粮食数据先于产量记录）
