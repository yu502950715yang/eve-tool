#  预警图片路径
import os
import sys


ALERT_IMG_PATH = "imgs/alert"
# 开发环境预警图片路径
DEV_ALERT_IMG_PATH = "../imgs/alert"
# 警报声音路径
ALERT_SOUND_PATH = "sounds/alarm.wav"
# 开发环境警报声音路径
DEV_ALERT_SOUND_PATH = "../sounds/alarm.wav"
# 配置文件路径
CONFIG_PATH = "config"
# 开发环境配置路径
DEV_CONFIG_PATH = "../config"

def _get_base_dir():
    return os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else \
           os.path.dirname(os.path.abspath(__file__))


def get_config_path(relative_path):
    """获取资源文件路径"""
    base_dir = _get_base_dir()
    path = CONFIG_PATH if getattr(sys, "frozen", False) else DEV_CONFIG_PATH
    config_path = os.path.normpath(os.path.join(base_dir, path))
    return os.path.normpath(os.path.join(config_path, relative_path))

def get_alert_img_path():
    """获取预警图片路径"""
    base_dir = _get_base_dir()
    path = ALERT_IMG_PATH if getattr(sys, "frozen", False) else DEV_ALERT_IMG_PATH
    return os.path.normpath(os.path.join(base_dir, path))

def get_alert_sound_path():
    """获取预警声音路径"""
    base_dir = _get_base_dir()
    path = ALERT_SOUND_PATH if getattr(sys, "frozen", False) else DEV_ALERT_SOUND_PATH
    return os.path.normpath(os.path.join(base_dir, path))