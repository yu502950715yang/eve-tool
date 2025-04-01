import tkinter as tk

import keyboard
import pyautogui
from PIL import ImageGrab, ImageTk


class PreviewWindow:
    def __init__(self, region, restart_callback, window_region=None):
        if window_region is None:
            window_region = [0, 0]
        self.restart_callback = restart_callback
        self.x, self.y = 0, 0
        """初始化预览窗口，设置窗口大小和画布"""
        self.region = region
        self.preview_window = tk.Tk()
        self.preview_window.title("eve-tool")
        # 设置窗口整体透明度（0.8为示例值，范围0-1）
        self.preview_window.attributes("-alpha", 0.95)
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
        self.preview_image = None
        self.restart_flag = False
        self.is_destroyed = False  # 标志窗口是否已经被销毁
        self.hotkeys = []  # 用于存储绑定的快捷键

    @staticmethod
    def handle_click(x, y):
        """处理点击事件，模拟鼠标点击"""
        print(f"处理点击事件: ({x}, {y})")
        pyautogui.click(x, y)
        pyautogui.PAUSE = 0.1
        pyautogui.doubleClick(x, y)

    def close(self, event=None):
        """关闭预览窗口"""
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
        if self.restart_flag:
            return
        try:
            screenshot = ImageGrab.grab(bbox=self.region)
            if screenshot.size == (0, 0):  # 检查无效截图
                raise Exception("Invalid screenshot")
        except Exception as e:
            print(f"截图失败: {e}")
            self.preview_window.after(1000, self.update_preview)  # 1秒后重试
            return
        self.preview_image = ImageTk.PhotoImage(screenshot)
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)
        self.preview_window.update()
        # 每50毫秒更新预览窗口
        self.preview_window.after(50, self.update_preview)

    def on_canvas_click(self, event):
        """处理画布点击事件，计算并输出点击的屏幕坐标"""
        screen_x = self.region[0] + event.x
        screen_y = self.region[1] + event.y
        print(f"点击屏幕坐标: ({screen_x}, {screen_y})")
        self.handle_click(screen_x, screen_y)

    def start(self):
        """启动预览窗口，绑定事件并开始更新循环"""
        # 左键点击
        self.preview_canvas.bind("<Button-1>", self.on_canvas_click)
        # 右键双击
        self.preview_canvas.bind("<Double-Button-3>", self.close)
        # 右键按下
        self.preview_canvas.bind("<ButtonPress-3>", self.on_canvas_press_right)
        # 右键拖动
        self.preview_canvas.bind("<B3-Motion>", self.move)
        # 绑定快捷键“·” 数字1旁边的按键
        hotkey1 = keyboard.add_hotkey("`", self.handle_center_click)
        self.hotkeys.append(hotkey1)
        # 绑定快捷键“ctrl+alt+r”重新选择监控区域
        hotkey2 = keyboard.add_hotkey("ctrl+alt+r", self.restart)
        self.hotkeys.append(hotkey2)
        self.update_preview()
        self.preview_window.mainloop()

    def restart(self):
        """重新选择监控区域"""
        self.restart_flag = True
        window_region = [self.preview_window.winfo_x(), self.preview_window.winfo_y()]
        self.preview_window.after(0, lambda: self.restart_callback(window_region))
        self.close()
