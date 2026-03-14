# Resource Manager 资源管理系统

一个专业的资源管理系统，基于 Flask 构建，为管理员和用户提供全面的资源管理功能。

## 功能特性

### 管理员功能
- **用户管理**：创建、编辑、删除和管理普通用户
- **资源操作**：为任意用户添加或减少资源
- **密码重置**：使用自定义值重置用户密码
- **兑换码管理**：生成或手动创建兑换码（8位字母数字组合）
- **操作日志**：跟踪所有操作及操作者信息
- **批量操作**：删除所有用户、清除日志、管理兑换码

### 普通用户功能
- **控制台**：查看资源余额（总计、已用、剩余）
- **资源兑换**：使用兑换码向账户添加资源
- **资源消耗**：消耗资源用于各种操作
- **个人信息管理**：更新用户名、邮箱和密码
- **历史记录**：查看个人操作历史

## 配置说明

### 资源类型设置

编辑 `settings.py` 文件来自定义资源类型：

```python
# 支持的类型: 'token', 'inference', 'image', 'api_call', 'credit', 'custom'
RESOURCE_TYPE = "token"
```

当 `RESOURCE_TYPE = "token"` 时，显示使用英文（因为这是LLM领域的专业术语）：
- Tokens / Add Tokens / Consume Tokens

其他类型使用中文：
- 推理次数 / 增加推理次数 / 消耗推理次数
- 图像生成次数 / 增加生成次数 / 消耗生成次数

### 可用资源类型

| 类型 | 英文显示 | 中文显示 | 单位 |
|------|----------|----------|------|
| token | Tokens | Tokens | 个 |
| inference | 推理次数 | Inference Calls | 次 |
| image | 图像生成次数 | Image Generations | 张 |
| api_call | API调用次数 | API Calls | 次 |
| credit | 额度 | Credit | 点 |
| custom | 配额 | Quota | 单位 |

## 技术栈

- **后端**：Flask (Python)
- **数据库**：MySQL + SQLAlchemy ORM
- **认证**：Flask-Login
- **表单**：Flask-WTF
- **前端**：HTML, CSS, JavaScript (Jinja2 模板)

## 环境要求

- Python 3.10+
- MySQL Server 5.7+
- pip 或 conda

## 安装部署

### 1. 克隆并配置

```bash
# 创建虚拟环境（使用conda）
conda create -n token_env python=3.10
conda activate token_env

# 或使用 venv
python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install flask flask-sqlalchemy flask-migrate flask-login flask-wtf pymysql cryptography
```

### 3. 配置应用

打开 `settings.py` 文件，修改以下配置：

```python
# 数据库名称
DATABASE_NAME = "token_db"

# 默认管理员账户（首次运行自动创建）
DEFAULT_ADMIN_USERNAME = "root"
DEFAULT_ADMIN_PASSWORD = "root123"
DEFAULT_ADMIN_EMAIL = "root@example.com"

# 资源类型: 'token', 'inference', 'image', 'api_call', 'credit', 'custom'
RESOURCE_TYPE = "token"
```

### 4. 启动应用

```bash
python app.py
```

应用会自动完成以下操作：
- 创建数据库（如果不存在）
- 创建所有数据表
- 创建默认管理员账户（根据 settings.py 中的配置）

访问地址：http://localhost:5000

## 项目结构

```
token_manager/
├── app.py                 # 主应用文件
├── config.py              # 配置文件
├── settings.py            # 资源类型和界面配置
├── models.py              # 数据库模型
├── forms.py               # 表单验证
├── requirements.txt       # Python 依赖
├── README.md              # 英文文档
├── README_CN.md           # 中文文档
├── auth/
│   └── __init__.py       # 认证蓝图
├── admin/
│   └── __init__.py       # 管理员蓝图
├── user/
│   └── __init__.py       # 用户蓝图
├── templates/              # HTML 模板
└── static/
    └── css/
```

## 使用指南

### 管理员操作

1. **添加用户**：在控制台点击 "+ 添加用户"
2. **编辑用户**：点击用户行的"编辑"，然后修改密码或资源
3. **删除用户**：点击用户行的"删除"（不能删除自己）
4. **生成兑换码**：进入"兑换码管理" → 输入数量和资源数 → 点击"生成兑换码"
5. **查看日志**：进入"操作记录"查看所有操作

### 普通用户操作

1. **查看资源**：在控制台查看资源余额
2. **兑换兑换码**：进入"兑换码兑换" → 输入8位兑换码 → 点击"兑换码兑换"
3. **编辑个人资料**：进入"个人信息" → 修改资料 → 点击"保存"
4. **修改密码**：进入"个人信息" → 输入新密码 → 点击"保存"

## 安全说明

- 密码使用 Werkzeug 安全函数加密存储
- 通过 Flask-WTF 启用 CSRF 保护
- 通过 Flask-Login 进行会话管理
- 管理员路由仅限管理员用户访问

## 许可证

本项目仅供学习和内部使用。
