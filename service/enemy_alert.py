import os
from threading import Thread
import threading
import cv2
import numpy as np
import winsound


from utils.path_util import get_alert_img_path, get_alert_sound_path
from utils.settings import Settings

settings = Settings()


class EnemyAlert:

    _instance = None

    def __new__(cls):
        """重写 __new__ 方法实现单例"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.templates = self.load_templates()
        self.match_threshold = settings.get_enemy_match_threshold()  # 匹配阈值
        self.is_playing = False
        self.play_lock = threading.Lock()  # 播放声音锁

    def preprocess_template(self, img):
        # img = cv2.GaussianBlur(img, (3, 3), 0)  # 高斯模糊
        # img = cv2.equalizeHist(img)             # 直方图均衡化
        return img

    def preprocess_screenshot(self, img):
        img = cv2.GaussianBlur(img, (1, 1), 0)  # 高斯模糊
        # img = cv2.Canny(img, threshold1=50, threshold2=150)  # 边缘检测
        return img

    def multi_scale_match(self, template, screenshot, threshold):
        scales = [0.8, 1.0, 1.2]  # 定义缩放比例
        for scale in scales:
            resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
            """
            匹配模式
            模式	                英文全称	        特点	        最佳匹配
            cv2.TM_SQDIFF	        平方差匹配	        差值越小越好	 最小值
            cv2.TM_SQDIFF_NORMED	归一化平方差匹配	差值越小越好      最小值
            cv2.TM_CCORR	        相关性匹配	        值越大越好	    最大值
            cv2.TM_CCORR_NORMED	    归一化相关性匹配	值越大越好	    最大值
            cv2.TM_CCOEFF	        相关系数匹配	    值越大越好	    最大值
            cv2.TM_CCOEFF_NORMED	归一化相关系数匹配	值越大越好	    最大值
            """
             # 对每个通道分别进行匹配
            result_b = cv2.matchTemplate(screenshot[:, :, 0], resized_template[:, :, 0], cv2.TM_CCOEFF_NORMED)
            result_g = cv2.matchTemplate(screenshot[:, :, 1], resized_template[:, :, 1], cv2.TM_CCOEFF_NORMED)
            result_r = cv2.matchTemplate(screenshot[:, :, 2], resized_template[:, :, 2], cv2.TM_CCOEFF_NORMED)
            result = (result_b + result_g + result_r) / 3.0
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > threshold:
                return True, max_val
            # if min_val < 0.1:
            #     return True, min_val
        return False, 0

    def load_templates(self):
        """加载模板图片并转为灰度图"""
        template_dir = get_alert_img_path()
        templates = {}
        if not os.path.exists(template_dir):
            print(f"警告：模板目录 {template_dir} 不存在")
            return templates
        for filename in os.listdir(template_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(template_dir, filename)
                img = cv2.imread(path)
                if img is not None:
                    img = self.preprocess_template(img)
                    templates[filename] = img
                else:
                    print(f"无法加载模板图片：{path}")
        return templates

    def check_enemy(self, screenshot):
        """检查是否有敌人"""
        # 转换为OpenCV格式
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        # color_screenshot = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
        color_screenshot = self.preprocess_screenshot(screenshot_cv)
        temp_play_flag = False
        for key, template in self.templates.items():
            match_found, max_val = self.multi_scale_match(
                template, color_screenshot, self.match_threshold
            )
            if match_found:
                print(f"文件名：{key}，匹配值：{max_val}")
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
