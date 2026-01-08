# Claude Code 全生命周期最佳实践指南

**项目配置**: Vue.js (前端) + FastAPI (后端) + PostgreSQL (数据库)
**学习重点**: AI协作开发
**Git工作流**: 半自动化 (Claude建议，用户审核)

---

## 第一阶段：项目初始化与蓝图规划

### 1.1 使用 Plan Mode 规划架构

```bash
# 进入计划模式，让Claude Code帮助设计整体架构
/plan
```

**规划内容应包含：**

- 项目目录结构
- API端点设计
- 数据库模型设计
- 前后端交互方式
- 认证授权方案
- Docker配置
- 测试策略

### 1.2 创建 CLAUDE.md 项目文档

```bash
/init
```

这会创建项目文档，记录：
- 项目架构决策
- 代码规范
- 开发约定
- API设计原则

### 1.3 推荐的目录结构

```
MyVibeCoding/
├── frontend/                 # Vue.js 前端
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── views/           # 页面
│   │   ├── api/             # API调用封装
│   │   ├── stores/          # Pinia状态管理
│   │   ├── router/          # 路由配置
│   │   └── assets/          # 静态资源
│   ├── package.json
│   └── vite.config.js
│
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   ├── api/             # API路由
│   │   ├── models/          # SQLAlchemy模型
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # 业务逻辑
│   │   ├── core/            # 核心配置
│   │   └── db/              # 数据库会话
│   ├── requirements.txt
│   └── pyproject.toml
│
├── database/                 # 数据库相关
│   ├── migrations/          # Alembic迁移
│   └── seeds/               # 种子数据
│
├── docker/                   # Docker配置
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── docker-compose.yml
│
├── tests/                    # 测试
│   ├── frontend/
│   ├── backend/
│   └── integration/
│
├── docs/                     # 文档
├── .claude/                  # Claude Code配置
├── CLAUDE.md                 # 项目文档(由/init生成)
└── README.md
```

---

## 第二阶段：开发流程最佳实践

### 2.1 功能开发工作流

```
1. /plan → 进入计划模式，规划功能实现
   ↓
2. Claude编写代码
   ↓
3. 人工review代码
   ↓
4. 运行测试
   ↓
5. /commit → 创建提交(半自动，需审核)
   ↓
6. git push
   ↓
7. gh pr create → 创建PR
```

### 2.2 与Claude交互的技巧

**好的Prompt示例：**
```
创建一个产品列表页面，包含：
- 使用Vue 3组合式API
- 支持分页(每页20条)
- 支持搜索和筛选
- 调用后端 GET /api/products
- 添加加载状态和错误处理
```

**避免的Prompt：**
```
"帮我写个页面" (太模糊)
"重写整个项目" (范围太大)
```

### 2.3 任务分解原则

- 每个任务应可在30分钟内完成
- 一个任务对应一个git commit
- 任务之间尽量解耦，便于并行开发

---

## 第三阶段：Git工作流（半自动化）

### 3.1 推荐的分支策略

```
main (生产)
  ↑
develop (开发)
  ↑
feature/xxx (功能分支)
bugfix/xxx (修复分支)
```

### 3.2 使用 /commit 创建提交

```bash
# 开发完成后，使用/commit命令
/commit
```

**Claude Code会：**
1. 运行 `git status` 查看变更
2. 运行 `git diff` 查看具体改动
3. 分析变更并生成提交信息
4. 等待你确认后才执行提交

**你只需要：**
- 审核生成的提交信息
- 确认或修改后执行提交

### 3.3 创建Pull Request

```bash
# 推送分支后
git push origin feature/product-list

# 让Claude帮你创建PR
gh pr create --title "添加产品列表功能" --body "..."
```

或者使用交互式：
```
帮我为当前分支创建一个PR，总结这次的变更内容
```

### 3.4 提交信息规范

Claude Code遵循 Conventional Commits：
```
feat: 添加产品列表页面
fix: 修复用户认证过期问题
docs: 更新API文档
refactor: 重构数据库连接池
test: 添加产品服务单元测试
```

---

## 第四阶段：测试策略

### 4.1 测试配置

**后端 (pytest):**
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=app --cov-report=html
```

**前端 (Vitest):**
```js
// vitest.config.js
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html']
    }
  }
})
```

### 4.2 让Claude运行测试

```bash
# 告诉Claude运行测试
运行后端测试
运行前端测试
运行全部测试并修复失败的用例
```

### 4.3 TDD工作流

```
1. 让Claude写测试（先写，会失败）
   ↓
2. 让Claude实现代码（让测试通过）
   ↓
3. 让Claude重构（优化代码）
   ↓
4. /commit
```

---

## 第五阶段：Docker与本地开发

### 5.1 docker-compose.yml

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000
    command: npm run dev -- --host

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://vibe:vibe@db:5432/vibedb
      - CORS_ORIGINS=http://localhost:5173
    depends_on:
      - db
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=vibe
      - POSTGRES_PASSWORD=vibe
      - POSTGRES_DB=vibedb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 5.2 开发环境启动

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 进入容器调试
docker-compose exec backend bash
```

---

## 第六阶段：高级技巧

### 6.1 使用Git Worktrees并行开发

```bash
# 创建多个工作树，同时开发多个功能
git worktree add ../feature-auth feature/auth
git worktree add ../bugfix-api bugfix/api

# 在不同的终端中分别进入不同目录
# 每个目录可以运行独立的Claude Code实例
cd ../feature-auth  # Claude Code实例1
cd ../bugfix-api    # Claude Code实例2
```

**优势：**
- 功能隔离，互不干扰
- 可以同时运行多个Claude Code实例
- 每个工作树有独立的git状态

### 6.2 Pre-commit钩子配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
        args: [--fix]
```

### 6.3 Claude Code配置

```json
// .claude/config.json
{
  "mcpServers": {
    "excel": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-excel"]
    }
  },
  "hooks": {
    "pre-write": "npm run format"
  }
}
```

---

## 第七阶段：实战步骤清单

### 第一步：初始化项目

- [ ] 创建仓库
- [ ] `/init` 创建项目文档
- [ ] `/plan` 规划项目架构
- [ ] 创建基础目录结构
- [ ] 配置 docker-compose.yml

### 第二步：后端开发
- [ ] 创建FastAPI项目结构
- [ ] 配置数据库连接
- [ ] 创建基础模型
- [ ] 实现CRUD API
- [ ] 添加测试
- [ ] `/commit` 提交

### 第三步：前端开发
- [ ] 创建Vue3项目
- [ ] 配置路由和状态管理
- [ ] 创建API客户端
- [ ] 实现页面组件
- [ ] 添加测试
- [ ] `/commit` 提交

### 第四步：集成
- [ ] 前后端联调
- [ ] Docker集成测试
- [ ] CI/CD配置
- [ ] 创建PR

---

## 常用命令速查

| 操作 | 命令/对话 |
|------|----------|
| 规划功能 | `/plan` 或 "进入计划模式" |
| 初始化文档 | `/init` |
| 创建提交 | `/commit` 或 "帮我提交这些改动" |
| 运行测试 | "运行测试" |
| 代码审查 | "review这段代码" |
| 解释代码 | "解释这个文件的作用" |
| 重构代码 | "重构xxx，使其更易维护" |
| 修复bug | "修复这个错误：[错误信息]" |
| 创建PR | "为当前分支创建PR" |

---

## 关键要点总结

1. **始终使用Plan Mode**：开始新功能前先规划
2. **小步快跑**：频繁提交，每个commit做一件事
3. **人工审核**：Claude生成的代码必须review
4. **测试驱动**：让Claude写测试，再写实现
5. **文档同步**：保持CLAUDE.md与代码同步更新
6. **利用Worktrees**：复杂功能可并行开发

---

## 学习路线建议

### 初级阶段（第1-2周）
1. 熟悉 `/plan` 和 `/commit` 基本命令
2. 完成简单的CRUD功能
3. 掌握基本的前后端交互

### 中级阶段（第3-4周）
1. 学习Docker容器化部署
2. 实现完整的认证授权
3. 编写单元测试和集成测试

### 高级阶段（第5-6周）
1. 使用Git Worktrees并行开发
2. 配置CI/CD自动化
3. 性能优化和安全加固

---

*这份指南将随着你的学习进度不断更新完善*
