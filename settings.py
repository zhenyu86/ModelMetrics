"""
Application Settings Configuration
==================================
This file contains all configurable settings for the application.
You can customize the resource names, display text, and other settings here.

Supported resource types:
- token: Tokens (professional term in LLM field)
- inference: Inference calls (for AI inference)
- image: Image generation calls
- api_call: API calls
- credit: Credit/Quota
- custom: Custom
"""

# =============================================================================
# PROJECT CONFIGURATION
# =============================================================================

# =============================================================================
# PROJECT CONFIGURATION
# =============================================================================

# Project name (displayed in title, navbar, etc.)
PROJECT_NAME = "Token 管理系统"

# Project short name (for compact displays)
PROJECT_SHORT_NAME = "TMS"

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Database name (will be auto-created if not exists)
DATABASE_NAME = "token_db"

# =============================================================================
# DEFAULT ADMIN CONFIGURATION
# =============================================================================

# Default admin username (will be auto-created on first run)
DEFAULT_ADMIN_USERNAME = "root"

# Default admin password (will be auto-created on first run)
DEFAULT_ADMIN_PASSWORD = "root123"

# Default admin email
DEFAULT_ADMIN_EMAIL = "root@example.com"

# =============================================================================
# RESOURCE CONFIGURATION
# =============================================================================

# Resource type: 'token', 'inference', 'image', 'api_call', 'credit', 'custom'
# This determines what the system manages
RESOURCE_TYPE = "inference"

# Resource display names - mixed Chinese and English for token (as it's a professional term in LLM field)
# Each industry should use consistent terminology
RESOURCE_NAMES = {
    "token": {
        "name": "Tokens",
        "name_plural": "Tokens",
        "unit": "个",
        "action_add": "增加 Tokens",
        "action_reduce": "扣减 Tokens",
        "action_consume": "消耗 Tokens",
    },
    "inference": {
        "name": "推理次数",
        "name_plural": "推理次数",
        "unit": "次",
        "action_add": "增加推理次数",
        "action_reduce": "扣减推理次数",
        "action_consume": "消耗推理次数",
    },
    "image": {
        "name": "图像生成次数",
        "name_plural": "图像生成次数",
        "unit": "张",
        "action_add": "增加生成次数",
        "action_reduce": "扣减生成次数",
        "action_consume": "消耗生成次数",
    },
    "api_call": {
        "name": "API调用次数",
        "name_plural": "API调用次数",
        "unit": "次",
        "action_add": "增加调用次数",
        "action_reduce": "扣减调用次数",
        "action_consume": "消耗调用次数",
    },
    "credit": {
        "name": "额度",
        "name_plural": "额度",
        "unit": "点",
        "action_add": "增加额度",
        "action_reduce": "扣减额度",
        "action_consume": "消耗额度",
    },
    "custom": {
        "name": "配额",
        "name_plural": "配额",
        "unit": "单位",
        "action_add": "增加配额",
        "action_reduce": "扣减配额",
        "action_consume": "消耗配额",
    },
}

# If RESOURCE_TYPE is 'custom', use these custom names
CUSTOM_RESOURCE_NAME = {
    "name": "资源",
    "name_plural": "资源",
    "unit": "个",
    "action_add": "增加资源",
    "action_reduce": "扣减资源",
    "action_consume": "消耗资源",
}

# =============================================================================
# VERIFICATION CODE SETTINGS
# =============================================================================

# Verification code display name
CODE_NAME = "兑换码"

# =============================================================================
# UI TEXT CONFIGURATION (all in Chinese)
# =============================================================================

UI_TEXT = {
    "login": "登录",
    "register": "注册",
    "logout": "退出",
    "dashboard": "控制台",
    "admin_panel": "管理面板",
    "user_management": "用户管理",
    "operation_logs": "操作记录",
    "verification_codes": "兑换码管理",
    "profile": "个人信息",
    "settings": "设置",
    "total": "总量",
    "used": "已使用",
    "remaining": "剩余",
    "usage": "使用情况",
    "add": "增加",
    "reduce": "扣减",
    "consume": "消耗",
    "add_resource": "添加",
    "reduce_resource": "扣减",
    "redeem_code": "兑换码兑换",
    "generate_code": "生成兑换码",
    "save": "保存",
    "cancel": "取消",
    "edit": "编辑",
    "delete": "删除",
    "confirm": "确认",
    "search": "搜索",
    "filter": "筛选",
    "export": "导出",
    "no_records": "暂无记录",
    "welcome": "欢迎",
    "usage_records": "使用记录",
    "recent_records": "最近记录",
    "view_all": "查看全部",
    "username": "用户名",
    "email": "邮箱",
    "password": "密码",
    "new_password": "新密码",
    "confirm_password": "确认密码",
    "remember": "记住我",
    "role": "角色",
    "admin": "管理员",
    "user": "普通用户",
    "status": "状态",
    "unused": "未使用",
    "used_status": "已使用",
    "created_at": "创建时间",
    "used_at": "使用时间",
    "operator": "操作者",
    "target_user": "被操作用户",
    "action_type": "操作类型",
    "amount": "数量",
    "description": "说明",
    "time": "时间",
    "clear": "清除",
    "back": "返回",
    "submit": "提交",
    "add_user": "添加用户",
    "edit_user": "编辑用户",
    "reset_password": "重置密码",
    "clear_records": "清除记录",
    "delete_user": "删除用户",
    "clear_used": "清除已使用",
    "user_logs": "用户日志",
    "all_logs": "全部记录",
    "quantity": "数量",
    "auto_generate": "自动生成",
    "manual_add": "手动添加",
}


def get_resource_config():
    """Get the current resource configuration based on RESOURCE_TYPE."""
    if RESOURCE_TYPE in RESOURCE_NAMES:
        return RESOURCE_NAMES[RESOURCE_TYPE]
    return CUSTOM_RESOURCE_NAME
