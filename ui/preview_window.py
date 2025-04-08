import tkinter as tk

import keyboard
import pyautogui
import threading
from PIL import ImageGrab, ImageTk

from service.enemy_alert import EnemyAlert


class PreviewWindow:
    def __init__(self, region, restart_callback, window_region=None):
        if window_region is None:
            window_region = [0, 0]
        self.restart_callback = restart_callback
        self.x, self.y = 0, 0
        # 初始化预览窗口，设置窗口大小和画布
        self.region = region
        self.preview_window = tk.Tk()
        self.preview_window.title("eve-tool")
        # 设置窗口整体透明度（0.8为示例值，范围0-1）
        self.preview_window.attributes("-alpha", 0.71)
        # 设置窗口置顶
        self.preview_window.attributes("-topmost", True)
        width = abs(region[2] - region[0])
        height = abs(region[3] - region[1])
        self.preview_window.geometry(
            f"{width}x{height}+{window_region[0]}+{window_region[1]}"
        )
        self.preview_window.overrideredirect(True)
        self.preview_canvas = tk.Canvas(self.preview_window)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_canvas.configure(highlightthickness=0, bd=0)
        self.preview_image = None
        self.restart_flag = False
        self.is_destroyed = False  # 标志窗口是否已经被销毁
        self.hotkeys = []  # 用于存储绑定的快捷键
        self.enemy_alarm_open = False  # 敌对报警开关
        self.enemy_alert = EnemyAlert()
        # 创建右键菜单
        self.context_menu = tk.Menu(self.preview_window, tearoff=0)
        self.create_context_menu()

    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu.add_command(label="重新选择区域", command=self.restart)
        self.context_menu.add_command(
            label="开启敌对报警", command=self.toggle_enemy_alarm
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(label="退出", command=self.close)

    def show_context_menu(self, event):
        """显示右键菜单"""
        current_label = "关闭敌对报警" if self.enemy_alarm_open else "开启敌对报警"
        self.context_menu.entryconfig(1, label=current_label)
        # 显示菜单并强制获取焦点
        self.context_menu.post(event.x_root, event.y_root)
        self.context_menu.focus_force()

    def toggle_enemy_alarm(self):
        """切换敌对报警状态"""
        print("切换敌对报警状态")
        if self.enemy_alarm_open:
            self.stop_enemy_alarm()
            self.context_menu.entryconfig(1, label="开启敌对报警")
        else:
            self.start_enemy_alarm()
            self.context_menu.entryconfig(1, label="关闭敌对报警")

    @staticmethod
    def handle_click(x, y):
        """处理点击事件，模拟鼠标点击"""
        print(f"处理点击事件: ({x}, {y})")
        pyautogui.click(x, y)
        pyautogui.PAUSE = 0.1
        pyautogui.doubleClick(x, y)

    def close(self, event=None):
        """关闭预览窗口"""
        if self.enemy_alarm_open:
            self.stop_enemy_alarm()

        if not self.is_destroyed:
            self.preview_window.destroy()
            self.is_destroyed = True
            # 取消绑定的快捷键
            for hotkey in self.hotkeys:
                keyboard.remove_hotkey(hotkey)

    def on_canvas_press_right(self, event):
        """记录右键按下时的初始坐标"""
        self.x = event.x
        self.y = event.y

    def move(self, event):
        """窗口移动事件（已修正坐标计算）"""
        new_x = self.preview_window.winfo_x() + (event.x - self.x)
        new_y = self.preview_window.winfo_y() + (event.y - self.y)
        self.preview_window.geometry(f"+{new_x}+{new_y}")

    def handle_center_click(self):
        """处理快捷键点击事件，传入窗口中心坐标"""
        center_x = self.region[0] + (self.region[2] - self.region[0]) // 2
        center_y = self.region[1] + (self.region[3] - self.region[1]) // 2
        self.handle_click(center_x, center_y)

    def update_preview(self):
        """更新预览窗口中的截图"""
        if self.restart_flag or self.is_destroyed:
            return
        def capture_screenshot():
            try:
                screenshot = ImageGrab.grab(bbox=self.region)
                if screenshot.size == (0, 0):  # 检查无效截图
                    raise Exception("Invalid screenshot")
                # 在主线程中更新画布
                self.preview_window.after(0, lambda: self.update_canvas(screenshot))
            except Exception as e:
                print(f"截图失败: {e}")
                self.preview_window.after(1000, self.update_preview)  # 1秒后重试
        threading.Thread(target=capture_screenshot, daemon=True).start()
        self.preview_window.after(100, self.update_preview)

    def update_canvas(self, screenshot):
        """在主线程中更新画布"""
        self.preview_image = ImageTk.PhotoImage(screenshot)
        self.preview_canvas.delete("all")  # 清除之前的图像，避免叠加
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)

    def on_canvas_click(self, event):
        """处理画布点击事件，计算并输出点击的屏幕坐标"""
        screen_x = self.region[0] + event.x
        screen_y = self.region[1] + event.y
        print(f"点击屏幕坐标: ({screen_x}, {screen_y})")
        self.handle_click(screen_x, screen_y)

    def start(self):
        """启动预览窗口，绑定事件并开始更新循环"""
        self.bind_hotkeys()
        self.update_preview()
        self.preview_window.mainloop()

    def restart(self):
        """重新选择监控区域"""
        self.restart_flag = True
        window_region = [self.preview_window.winfo_x(), self.preview_window.winfo_y()]
        self.preview_window.after(0, lambda: self.restart_callback(window_region))
        self.preview_window.after(100, self.close)  # 关闭当前窗口

    def start_enemy_alarm(self):
        """开启敌对报警"""
        if self.enemy_alarm_open:
            return
        self.enemy_alarm_open = True
        print("开始敌对报警")
        self.check_enemy()

    def stop_enemy_alarm(self):
        """关闭敌对报警"""
        if not self.enemy_alarm_open:
            return
        self.enemy_alarm_open = False
        print("关闭敌对报警")

    def check_enemy(self):
        """检测是否有敌对"""
        print(f"========检测是否有敌对========{self.enemy_alarm_open}")
        if not self.enemy_alarm_open or self.restart_flag:
            return
        try:
            screenshot = ImageGrab.grab(bbox=self.region)
            if screenshot.size == (0, 0):  # 检查无效截图
                raise Exception("Invalid screenshot")
        except Exception as e:
            print(f"截图失败: {e}")
            self.preview_window.after(3000, self.check_enemy)
            return
        self.enemy_alert.check_enemy(screenshot)
        self.preview_window.after(2000, self.check_enemy)

    def bind_hotkeys(self):
        """绑定快捷键"""
        self.preview_canvas.bind("<ButtonPress-1>", self.on_canvas_press_right)
        self.preview_canvas.bind("<B1-Motion>", self.move)
        self.preview_canvas.bind("<Button-3>", self.show_context_menu)
        hotkeys = {
            "`": self.handle_center_click,  # 快捷键：点击中心点
            "ctrl+alt+r": self.restart,  # 快捷键：重新选择区域
            "ctrl+alt+1": self.start_enemy_alarm,  # 快捷键：开启敌对报警
            "ctrl+alt+2": self.stop_enemy_alarm,  # 快捷键：关闭敌对报警
            "ctrl+alt+m": self.preview_window.withdraw,  # 快捷键：最小化窗口
            "ctrl+alt+n": self.preview_window.deiconify,  # 快捷键：恢复窗口
        }
        for key, action in hotkeys.items():
            hotkey = keyboard.add_hotkey(key, action)
            self.hotkeys.append(hotkey)
