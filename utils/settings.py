import json
import os

from utils.path_util import get_config_path

DEFAULT_SETTINGS = {"monitor_region": [0, 0, 0, 0], "enemy_match_threshold": 0.8}


class Settings:

    # 单例模式
    _instance = None

    def __new__(cls):
        """重写 __new__ 方法实现单例"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.settings = DEFAULT_SETTINGS
        return cls._instance
    
    def __init__(self):
        self.settings = self.read_local_config()

    def get_monitor_region(self):
        """获取监控区域的设置"""
        return self.settings.get("monitor_region")
    
    def get_enemy_match_threshold(self):
        """获取匹配阈值的设置"""
        return self.settings.get("enemy_match_threshold")

    def save_monitor_region(self, monitor_region):
        """保存监控区域的设置"""
        self.settings["monitor_region"] = monitor_region
        setting_path = get_config_path("settings.json")
        # 如果不存在创建一个
        os.makedirs(os.path.dirname(setting_path), exist_ok=True)
        try:
            with open(setting_path, "w", encoding="utf-8") as config_file:
                json.dump(self.settings, config_file, indent=4)

        except Exception as e:
            print(
                f"保存配置文件失败 | 路径: {setting_path} | 错误类型: {type(e).__name__} | 详细信息: {str(e)}"
            )

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