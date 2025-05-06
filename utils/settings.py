import json
import os

from utils.path_util import get_config_path
from utils.singleton import Singleton

# 默认配置
DEFAULT_SETTINGS = {
    "monitor_region": [0, 0, 0, 0],
    "enemy_match_threshold": 0.1,
    "windows_region": [0, 0],
    "qb": {
        "triggerHotkey": "Ctrl+Shift+F1",
        "sendKey": "F1",
        "delayBetween": 100,
        "requireActivation": 1,
        "windows": ["军用馒头", "隔壁老王", "新建文本文档", "识田间-平台端"]
    }
}

class Settings(metaclass=Singleton):
    """使用元类实现的单例模式设置类"""
    
    def __init__(self):
        self.settings = DEFAULT_SETTINGS
        self.settings = self.read_local_config()

    def get_monitor_region(self):
        """获取监控区域的设置"""
        return self.settings.get("monitor_region")

    def get_enemy_match_threshold(self):
        """获取匹配阈值的设置"""
        return self.settings.get("enemy_match_threshold")
    
    def get_windows_region(self):
        """获取窗口区域的设置"""
        return self.settings.get("windows_region")

    def save_monitor_region(self, monitor_region):
        """保存监控区域的设置"""
        self.settings["monitor_region"] = monitor_region
        self._save_settings()
    
    def save_windows_region(self, windows_region):
        """保存窗口区域的设置"""
        self.settings["windows_region"] = windows_region
        self._save_settings()

    def get_qb_settings(self):
        """获取qb的设置"""
        return self.settings.get("qb")
    
    def get_qb_trigger_hotkey(self):
        """获取qb的触发热键设置"""
        return self.settings["qb"].get("triggerHotkey")
    
    def get_qb_send_key(self):
        """获取qb的发送按键设置"""
        return self.settings["qb"].get("sendKey")

    def merge_settings_with_defaults(self, settings, defaults=None):
        """Merge the loaded settings with the default settings recursively."""
        if defaults is None:
            defaults = self.settings
        merged_settings = defaults.copy()
        for key, value in defaults.items():
            if key in settings:
                if isinstance(value, dict) and isinstance(settings[key], dict):
                    # Rekursiv verschachtelte Dictionaries zusammenführen
                    merged_settings[key] = self.merge_settings_with_defaults(
                        settings[key], value
                    )
                else:
                    merged_settings[key] = settings[key]
            else:
                # Fehlende Schlüssel mit Standardwerten ergänzen
                merged_settings[key] = value
        return merged_settings

    def read_local_config(self):
        """读取本地配置文件"""
        setting_path = get_config_path("settings.json")
        print(f"读取配置文件: {setting_path}")
        try:
            with open(setting_path, encoding="utf-8") as config_file:
                settings = json.load(config_file)
                settings = self.merge_settings_with_defaults(settings)
        except:
            settings = DEFAULT_SETTINGS
        return settings

    def _save_settings(self):
        """保存配置文件"""
        setting_path = get_config_path("settings.json")
         # 如果不存在创建一个
        os.makedirs(os.path.dirname(setting_path), exist_ok=True)
        try:
            with open(setting_path, "w", encoding="utf-8") as config_file:
                json.dump(self.settings, config_file, ensure_ascii=False, indent=4)

        except Exception as e:
            print(
                f"保存配置文件失败 | 路径: {setting_path} | 错误类型: {type(e).__name__} | 详细信息: {str(e)}"
            )