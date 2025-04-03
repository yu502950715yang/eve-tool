import os
from threading import Thread
import threading
import cv2
import numpy as np

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
        self.match_threshold = 0.85  # 匹配阈值
        self.is_playing = False
        self.play_lock = threading.Lock()  # 播放声音锁

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
            print("检测到敌人")
            self.play_alert_sound()
        else:
            self.is_playing = False
            print("没有检测到敌人")

    def play_alert_sound(self):
        """非阻塞播放且避免重复播放"""
        def _play():
            try:
                with self.play_lock:
                    if self.is_playing:
                        return
                    self.is_playing = True

                import winsound
                print("播放预警")
                winsound.PlaySound(
                    get_alert_sound_path(), winsound.SND_FILENAME | winsound.SND_ASYNC
                )
            except Exception as e:
                print(f"播放失败：{str(e)}")
            finally:
                with self.play_lock:
                    self.is_playing = False
        # 仅在非播放状态时启动新线程
        with self.play_lock:
            if not self.is_playing:
                Thread(target=_play, daemon=True).start()
