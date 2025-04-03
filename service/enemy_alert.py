import os
import cv2
import numpy as np
from playsound import playsound

from utils.path_util import get_alert_img_path, get_alert_sound_path


class EnemyAlert:

    _instance = None

    def __new__(cls):
        """重写 __new__ 方法实现单例"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.templates = self.load_templates()
        self.match_threshold = 0.8  # 匹配阈值
        self.play_sound = False

    def load_templates(self):
        """加载模板图片并转为灰度图"""
        template_dir = get_alert_img_path()
        templates = []
        if not os.path.exists(template_dir):
            print(f"警告：模板目录 {template_dir} 不存在")
            return templates
        for filename in os.listdir(template_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(template_dir, filename)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    templates.append(img)
                else:
                    print(f"无法加载模板图片：{path}")
        return templates

    def check_enemy(self, screenshot):
        """检查是否有敌人"""
        # 转换为OpenCV格式并灰度化
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray_screenshot = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
        temp_play_flag = False
        for template in self.templates:
            result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val > self.match_threshold:
                print(f"检测到敌人，匹配值：{max_val}")
                temp_play_flag = True
                break
        if temp_play_flag:
            print("检测到敌人播放声音")
            self.play_alert_sound()
        else:
            self.play_sound = False
            print("没有检测到敌人,关闭声音")

    async def play_alert_sound(self):
        """播放警报声音"""
        try:
            await playsound(get_alert_sound_path())
        except Exception as e:
            print(f"播放声音失败: {e}")
