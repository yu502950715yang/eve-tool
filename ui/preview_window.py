import pyautogui
from PIL import ImageGrab, ImageTk
import tkinter as tk
import keyboard


class PreviewWindow:
    def __init__(self, region):
        """初始化预览窗口，设置窗口大小和画布"""
        self.region = region
        self.preview_window = tk.Tk()
        self.preview_window.title("eve-tool")
        # 设置窗口置顶
        self.preview_window.attributes('-topmost', True)
        width = abs(region[2] - region[0])
        height = abs(region[3] - region[1])
        self.preview_window.geometry(f"{width}x{height}")
        self.preview_canvas = tk.Canvas(self.preview_window)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_image = None
        # 绑定快捷键“·” 数字1旁边的按键
        keyboard.add_hotkey('`', self.handle_center_click)

    @staticmethod
    def handle_click(x, y):
        """处理点击事件，模拟鼠标点击"""
        print(f"处理点击事件: ({x}, {y})")
        pyautogui.click(x, y)
        pyautogui.PAUSE = 0.1
        pyautogui.doubleClick(x, y)

    def handle_center_click(self):
        """处理快捷键点击事件，传入窗口中心坐标"""
        center_x = self.region[0] + (self.region[2] - self.region[0]) // 2
        center_y = self.region[1] + (self.region[3] - self.region[1]) // 2
        self.handle_click(center_x, center_y)

    def update_preview(self):
        """更新预览窗口中的截图"""
        screenshot = ImageGrab.grab(bbox=self.region)
        self.preview_image = ImageTk.PhotoImage(screenshot)
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)
        self.preview_window.update()
        # 每10毫秒更新预览窗口
        self.preview_window.after(10, self.update_preview)

    def on_canvas_click(self, event):
        """处理画布点击事件，计算并输出点击的屏幕坐标"""
        screen_x = self.region[0] + event.x
        screen_y = self.region[1] + event.y
        print(f"点击屏幕坐标: ({screen_x}, {screen_y})")
        self.handle_click(screen_x, screen_y)

    def start(self):
        """启动预览窗口，绑定事件并开始更新循环"""
        self.preview_canvas.bind("<Button-1>", self.on_canvas_click)
        self.update_preview()
        self.preview_window.mainloop()
