import tkinter as tk
import tkinter.messagebox as messagebox
from screeninfo import get_monitors


class ScreenRegionSelector:
    def __init__(self):
        """初始化屏幕区域选择器，设置初始坐标和Tkinter窗口"""
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.monitors = get_monitors() #获取所有可用屏幕信息
        self.root = tk.Tk()
        # 设置窗口置顶
        self.root.attributes("-topmost", True)
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda event: self.handle_esc())
        self.rect = None
        self.root.focus_force()

    def on_button_press(self, event):
        """处理鼠标按下事件，记录起始坐标并绘制矩形"""
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            fill="blue",
            stipple="gray12",
        )

    def on_mouse_drag(self, event):
        """处理鼠标拖动事件，更新矩形的大小"""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        """处理鼠标释放事件，记录结束坐标并关闭窗口"""
        self.end_x = event.x
        self.end_y = event.y
        self.root.destroy()

    def handle_esc(self):
        """处理 Esc 键按下事件"""
        print("取消选择区域")
        self.root.destroy()

    def select_region(self):
        """启动全屏窗口，允许用户选择屏幕区域，并返回选中的区域坐标"""
        esc_pressed = False
        while True:
            # 计算覆盖所有屏幕的总区域
            min_x = min(monitor.x for monitor in self.monitors)
            min_y = min(monitor.y for monitor in self.monitors)
            max_x = max(monitor.x + monitor.width for monitor in self.monitors)
            max_y = max(monitor.y + monitor.height for monitor in self.monitors)

            # 启动全屏窗口
            self.root.geometry(f"{max_x - min_x}x{max_y - min_y}+{min_x}+{min_y}")
            self.root.attributes("-fullscreen", False)
            self.root.overrideredirect(True)  # 无边框窗口
            self.root.attributes("-alpha", 0.3)
            self.root.mainloop()

            if self.start_x is None or self.start_y is None or self.end_x is None or self.end_y is None:
                esc_pressed = True
                break
    
            # 检查是否选择了有效区域
            width = abs(self.end_x - self.start_x)
            height = abs(self.end_y - self.start_y)
    
            if width < 15 or height < 15:
                # 弹出提示框
                messagebox.showwarning("无效区域", "选择的区域过小，请重新选择！")
                # 重新初始化窗口
                self.__init__()
            else:
                break
        if esc_pressed:
            print("用户取消了选择")
            return None
        # 返回有效区域
        return [self.start_x, self.start_y, self.end_x, self.end_y]
