import os
import sys

RESOURCE_PATHS = {
    "alert_img": {"dev": "../imgs/alert", "prod": "imgs/alert"},
    "alert_sound": {"dev": "../sounds/alarm.wav", "prod": "sounds/alarm.wav"},
    "config": {"dev": "../config", "prod": "config"},
}

def is_frozen() -> bool:
    """判断程序是否是打包后的运行环境"""
    return getattr(sys, "frozen", False)

def _get_base_dir() -> str:
    """获取基础目录"""
    return os.path.dirname(sys.executable) if is_frozen() else \
           os.path.dirname(os.path.abspath(__file__))

def get_resource_path(resource_key: str) -> str:
    """通用资源路径获取函数"""
    base_dir = _get_base_dir()
    paths = RESOURCE_PATHS[resource_key]
    path = paths["prod"] if is_frozen() else paths["dev"]
    return os.path.normpath(os.path.join(base_dir, path))

def get_config_path(relative_path: str) -> str:
    """获取配置文件路径"""
    config_base_path = get_resource_path("config")
    return os.path.normpath(os.path.join(config_base_path, relative_path))

def get_alert_img_path() -> str:
    """获取预警图片路径"""
    return get_resource_path("alert_img")

def get_alert_sound_path() -> str:
    """获取预警声音路径"""
    return get_resource_path("alert_sound")