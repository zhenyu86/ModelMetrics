import os
from settings import (
    PROJECT_NAME,
    PROJECT_SHORT_NAME,
    RESOURCE_TYPE,
    get_resource_config,
    UI_TEXT,
    CODE_NAME,
    DATABASE_NAME,
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_EMAIL,
)


class Config:
    """Application configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:123456@localhost:3306/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_VIEW = 'auth.login'

    # Project settings (accessible in templates)
    PROJECT_NAME = PROJECT_NAME
    PROJECT_SHORT_NAME = PROJECT_SHORT_NAME
    RESOURCE_TYPE = RESOURCE_TYPE

    # Get resource config
    _resource_config = get_resource_config()
    RESOURCE_NAME = _resource_config["name"]
    RESOURCE_NAME_PLURAL = _resource_config["name_plural"]
    RESOURCE_UNIT = _resource_config["unit"]
    ACTION_ADD = _resource_config["action_add"]
    ACTION_REDUCE = _resource_config["action_reduce"]
    ACTION_CONSUME = _resource_config["action_consume"]

    # UI text (all in Chinese)
    UI_TEXT = UI_TEXT

    # Code name
    CODE_NAME = CODE_NAME
