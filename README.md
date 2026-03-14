# Resource Manager

A professional Resource Management System built with Flask, providing comprehensive resource management for administrators and users.

## Features

### For Administrators
- **User Management**: Create, edit, delete, and manage regular users
- **Resource Operations**: Add or reduce resources for any user
- **Password Reset**: Reset user passwords with custom values
- **Verification Codes**: Generate or manually create redemption codes (8-character alphanumeric)
- **Operation Logs**: Track all operations with operator information
- **Bulk Operations**: Delete all users, clear logs, manage verification codes

### For Regular Users
- **Dashboard**: View resource balance (total, used, remaining)
- **Resource Redemption**: Use verification codes to add resources to account
- **Resource Consumption**: Consume resources for various operations
- **Profile Management**: Update username, email, and password
- **History**: View personal operation history

## Configuration

### Resource Type Settings

Edit `settings.py` to customize the resource type:

```python
# Supported types: 'token', 'inference', 'image', 'api_call', 'credit', 'custom'
RESOURCE_TYPE = "token"
```

When `RESOURCE_TYPE = "token"`, the display will use English (as it's a professional term in LLM field):
- Tokens / Add Tokens / Consume Tokens

For other types, Chinese will be used:
- 推理次数 / 增加推理次数 / 消耗推理次数
- 图像生成次数 / 增加生成次数 / 消耗生成次数

### Available Resource Types

| Type | Display Name (EN) | Display Name (CN) | Unit |
|------|-------------------|-------------------|------|
| token | Tokens | Tokens | 个 |
| inference | 推理次数 | Inference Calls | 次 |
| image | 图像生成次数 | Image Generations | 张 |
| api_call | API调用次数 | API Calls | 次 |
| credit | 额度 | Credit | 点 |
| custom | 配额 | Quota | 单位 |

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Frontend**: HTML, CSS, JavaScript (Jinja2 templates)

## Prerequisites

- Python 3.10+
- MySQL Server 5.7+
- pip or conda

## Installation

### 1. Clone and Setup

```bash
# Create virtual environment
conda create -n token_env python=3.10
conda activate token_env

# Or using venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-migrate flask-login flask-wtf pymysql cryptography
```

### 3. Configure Application

Open `settings.py` and modify the following settings as needed:

```python
# Database name
DATABASE_NAME = "token_db"

# Default admin user (auto-created on first run)
DEFAULT_ADMIN_USERNAME = "root"
DEFAULT_ADMIN_PASSWORD = "root123"
DEFAULT_ADMIN_EMAIL = "root@example.com"

# Resource type: 'token', 'inference', 'image', 'api_call', 'credit', 'custom'
RESOURCE_TYPE = "token"
```

### 4. Run the Application

```bash
python app.py
```

The application will automatically:
- Create the database if it doesn't exist
- Create all required tables
- Create default admin user (as configured in settings.py)

Access the application at: http://localhost:5000

## Project Structure

```
token_manager/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── settings.py            # Resource type and UI settings
├── models.py              # Database models
├── forms.py               # WTForms for validation
├── requirements.txt       # Python dependencies
├── README.md              # English documentation
├── README_CN.md           # Chinese documentation
├── auth/
│   └── __init__.py       # Authentication blueprint
├── admin/
│   └── __init__.py       # Admin blueprint
├── user/
│   └── __init__.py       # User blueprint
├── templates/             # HTML templates
└── static/
    └── css/
```

## Usage Guide

### Admin Operations

1. **Add User**: Click "+ 添加用户" on the dashboard
2. **Edit User**: Click "编辑" on user row, then modify password or resources
3. **Delete User**: Click "删除" on user row (cannot delete yourself)
4. **Generate Codes**: Go to "兑换码管理" → Enter quantity and amount → Click "生成兑换码"
5. **View Logs**: Go to "操作记录" to see all operations

### User Operations

1. **View Resources**: Check dashboard for resource balance
2. **Redeem Code**: Go to "兑换码兑换" → Enter 8-character code → Click "兑换码兑换"
3. **Edit Profile**: Go to "个人信息" → Modify details → Click "保存"
4. **Change Password**: Go to "个人信息" → Enter new password → Click "保存"

## Security

- Passwords are hashed using Werkzeug's security functions
- CSRF protection enabled via Flask-WTF
- Session management via Flask-Login
- Admin routes restricted to admin users only

## License

This project is for educational and internal use purposes.
