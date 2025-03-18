import tkinter as tk

import pyautogui
from PIL import ImageGrab, ImageTk


class ScreenRegionSelector:
    def __init__(self):
        """初始化屏幕区域选择器，设置初始坐标和Tkinter窗口"""
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.rect = None

    def on_button_press(self, event):
        """处理鼠标按下事件，记录起始坐标并绘制矩形"""
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red',
                                                 fill='blue', stipple='gray12')

    def on_mouse_drag(self, event):
        """处理鼠标拖动事件，更新矩形的大小"""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        """处理鼠标释放事件，记录结束坐标并关闭窗口"""
        self.end_x = event.x
        self.end_y = event.y
        self.root.destroy()

    def select_region(self):
        """启动全屏窗口，允许用户选择屏幕区域，并返回选中的区域坐标"""
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.mainloop()
        if self.start_x is not None and self.end_x is not None:
            return self.start_x, self.start_y, self.end_x, self.end_y
        return None


def handle_click(x, y):
    """处理点击事件，模拟鼠标点击"""
    print(f"处理点击事件: ({x}, {y})")
    pyautogui.click(x, y)
    pyautogui.doubleClick(x, y)


class PreviewWindow:
    def __init__(self, region):
        """初始化预览窗口，设置窗口大小和画布"""
        self.region = region
        self.preview_window = tk.Tk()
        self.preview_window.title("Screen Preview")
        self.preview_window.attributes('-topmost', True)
        width = abs(region[2] - region[0])
        height = abs(region[3] - region[1])
        self.preview_window.geometry(f"{width}x{height}")
        self.preview_canvas = tk.Canvas(self.preview_window)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_image = None

    def update_preview(self):
        """更新预览窗口中的截图"""
        screenshot = ImageGrab.grab(bbox=self.region)
        self.preview_image = ImageTk.PhotoImage(screenshot)
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)
        self.preview_window.update()
        self.preview_window.after(10, self.update_preview)

    def on_canvas_click(self, event):
        """处理画布点击事件，计算并输出点击的屏幕坐标"""
        screen_x = self.region[0] + event.x
        screen_y = self.region[1] + event.y
        print(f"点击屏幕坐标: ({screen_x}, {screen_y})")
        handle_click(screen_x, screen_y)

    def start(self):
        """启动预览窗口，绑定事件并开始更新循环"""
        self.preview_canvas.bind("<Button-1>", self.on_canvas_click)
        self.update_preview()
        self.preview_window.mainloop()


def get_selected_region():
    """获取用户选择的屏幕区域，并启动预览窗口"""
    selector = ScreenRegionSelector()
    region = selector.select_region()
    if region:
        print(f"选中区域坐标: {region}")
        preview = PreviewWindow(region)
        preview.start()
    else:
        print("没有选择区域")
    return region


# Example usage
if __name__ == "__main__":
    selected_region = get_selected_region()
