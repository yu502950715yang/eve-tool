import tkinter as tk


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
