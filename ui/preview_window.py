from asyncio.windows_events import NULL
import time
import tkinter as tk

import webbrowser
from tkinter import messagebox

import keyboard
import pyautogui
import threading
from PIL import ImageGrab, ImageTk, Image

from service.enemy_alert import EnemyAlert
from service.sync_script import get_matched_windows, get_window_title, send_key_to_eve_window
from ui.setting_window import SettingsApp
from utils.settings import Settings

class PreviewWindow:

    settings = Settings()

    def __init__(self, region, restart_callback, window_region=None):
        if window_region is None:
            window_region = [0, 0]
        self.restart_callback = restart_callback
        self.x, self.y = 0, 0
        self.original_width = abs(region[2] - region[0])
        self.original_height = abs(region[3] - region[1])
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
        # self.preview_window.overrideredirect(True)
        self.preview_canvas = tk.Canvas(self.preview_window)
        self.preview_canvas.pack()
        self.preview_canvas.configure(highlightthickness=0, bd=0)

        self.preview_image = None
        self.restart_flag = False
        self.is_destroyed = False  # 标志窗口是否已经被销毁
        self.hotkeys = []  # 用于存储绑定的快捷键
        self.enemy_alarm_open = False  # 敌对报警开关
        self.sync_script_open = False  # 同步脚本开关
        self.enemy_alert = NULL  # 敌对报警实例
        # 创建右键菜单
        self.context_menu = tk.Menu(self.preview_window, tearoff=0)
        self.create_context_menu()
        self.preview_window_update_time = 100  # 更新频率
        self.check_enemy_time = 1500  # 敌对警报检查频率
        # 添加圆角边框和边框效果
        self.preview_window.configure(bg="#2b2b2b")
        self.preview_canvas.configure(
            bg="#2b2b2b", highlightthickness=1, highlightbackground="#404040"
        )
        # 添加状态指示器
        self.status_frame = tk.Frame(self.preview_window, bg="#2b2b2b")
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)
        # 添加状态指示灯
        self.enemy_status = tk.Canvas(
            self.status_frame, width=10, height=10, bg="#2b2b2b", highlightthickness=0
        )
        self.enemy_status.pack(side=tk.LEFT, padx=2)
        self.enemy_status.create_oval(2, 2, 8, 8, fill="gray", tags="status")

    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(
            self.preview_window,
            tearoff=0,
            bg="#2b2b2b",
            fg="white",
            activebackground="#404040",
            activeforeground="white",
        )
        # 添加图标支持
        self.context_menu.add_command(label="🔄 重新选择区域", command=self.restart)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="⚠️ 开启敌对报警", command=self.toggle_enemy_alarm)
        self.context_menu.add_command(label="💪 开启同步脚本", command=self.sync_script)
        self.context_menu.add_command(label="⚙️ 配置设置", command=self.open_settings)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🌐 kb网", command=lambda: self.openUrl('https://kb.ceve-market.org'))
        self.context_menu.add_command(label="🛒 市场中心", command=lambda: self.openUrl('https://www.ceve-market.org'))
        self.context_menu.add_command(label="🔧 EVE 小工具集", command=lambda: self.openUrl('https://tools.ceve-market.org/'))
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="🔻 后台运行(ctrl+alt+n重新显示)", command=self.preview_window.withdraw
        )
        self.context_menu.add_command(label="❌ 退出", command=self.close)

    def show_context_menu(self, event):
        """显示右键菜单"""
        current_label = "⚠️ 关闭敌对报警" if self.enemy_alarm_open else "⚠️ 开启敌对报警"
        self.context_menu.entryconfig(2, label=current_label)
        current_label = (
            "💪 关闭同步脚本" if self.sync_script_open else "💪 开启同步脚本"
        )
        self.context_menu.entryconfig(3, label=current_label)
        # 显示菜单并强制获取焦点
        self.context_menu.post(event.x_root, event.y_root)
        self.context_menu.focus_force()

    def update_status_indicators(self):
        """更新状态指示器"""
        enemy_color = "#00ff00" if self.enemy_alarm_open else "gray"
        self.enemy_status.itemconfig("status", fill=enemy_color)

    def toggle_enemy_alarm(self):
        """切换敌对报警状态"""
        print("切换敌对报警状态")
        if self.enemy_alarm_open:
            self.stop_enemy_alarm()
        else:
            self.start_enemy_alarm()
            self.update_status_indicators()

    @staticmethod
    def handle_click(x, y):
        """处理点击事件，模拟鼠标点击"""
        print(f"处理点击事件: ({x}, {y})")
        pyautogui.click(x, y)
        pyautogui.PAUSE = 0.1
        pyautogui.doubleClick(x, y)

    def close(self, event=None):
        """关闭预览窗口"""
        window_region = [self.preview_window.winfo_x(), self.preview_window.winfo_y()]
        self.settings.save_windows_region(window_region)
        if self.enemy_alarm_open:
            self.stop_enemy_alarm()

        if not self.is_destroyed:
            self.preview_window.destroy()
            self.is_destroyed = True
            # 取消绑定的快捷键
            keyboard.remove_all_hotkeys()

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
            error_flag = False
            try:
                screenshot = ImageGrab.grab(bbox=self.region)
                if screenshot.size == (0, 0):  # 检查无效截图
                    raise Exception("Invalid screenshot")
                # 在主线程中更新画布
                self.preview_window.after(0, lambda: self.update_canvas(screenshot))
            except Exception as e:
                print(f"截图失败: {e}")
                error_flag = True
            finally:
                self.preview_window_update_time = 1000 if error_flag else 100

        threading.Thread(target=capture_screenshot, daemon=True).start()
        self.preview_window.after(self.preview_window_update_time, self.update_preview)

    def update_canvas(self, screenshot):
        """在主线程中更新画布"""
        # 获取画布当前尺寸
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        # 获取截图原始尺寸
        original_width, original_height = screenshot.size

        # 计算缩放比例（保持宽高比）
        scale = min(canvas_width / original_width, canvas_height / original_height)
        new_size = (int(original_width * scale), int(original_height * scale))

        # 缩放图像（使用双线性插值提高质量）
        resized_image = screenshot.resize(new_size, Image.Resampling.BILINEAR)

        #转换为Tkinter兼容格式
        self.preview_image = ImageTk.PhotoImage(resized_image)

        # self.preview_image = ImageTk.PhotoImage(screenshot)
        self.preview_canvas.delete("all")  # 清除之前的图像，避免叠加
        x_center = (canvas_width - new_size[0]) // 2
        y_center = (canvas_height - new_size[1]) // 2
        self.preview_canvas.create_image(x_center, y_center, anchor=tk.NW, image=self.preview_image)

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
        self.enemy_alert = EnemyAlert()
        self.enemy_alarm_open = True
        print("开始敌对报警")
        self.check_enemy()

    def stop_enemy_alarm(self):
        """关闭敌对报警"""
        if not self.enemy_alarm_open:
            return
        self.enemy_alert = NULL
        self.enemy_alarm_open = False
        print("关闭敌对报警")

    def check_enemy(self):
        """检测是否有敌对"""
        print(f"========检测是否有敌对========{self.enemy_alarm_open}")
        if not self.enemy_alarm_open or self.restart_flag:
            return

        def capture_screenshot():
            error_flag = False
            try:
                screenshot = ImageGrab.grab(bbox=self.region)
                if screenshot.size == (0, 0):  # 检查无效截图
                    raise Exception("Invalid screenshot")
                self.enemy_alert.check_enemy(screenshot)
            except Exception as e:
                print(f"截图失败: {e}")
                error_flag = True
            finally:
                self.check_enemy_time = 3000 if error_flag else 1500

        threading.Thread(target=capture_screenshot, daemon=True).start()
        self.preview_window.after(self.check_enemy_time, self.check_enemy)

    def sync_script(self):
        """开启关闭同步脚本"""
        triggerHotkey = self.settings.get_qb_trigger_hotkey()
        if self.sync_script_open:
            self.sync_script_open = False
            # 取消快捷键绑定
            keyboard.remove_hotkey(triggerHotkey)
            print("关闭同步脚本")
            return
        self.sync_script_open = True
        print("开启同步脚本")
        eve_windows = get_matched_windows()
        # 间隔时间
        sleep_time = self.settings.get_qb_delay_between() / 1000
        if eve_windows:
            eve_windows_title = get_window_title(eve_windows)
            messagebox.showinfo(
                "提示",
                f"找到匹配窗口:\n {'\n '.join(eve_windows_title)}\n\n请按下快捷键: {triggerHotkey}",
            )
            # 绑定快捷键
            keyboard.add_hotkey(
                triggerHotkey,
                self.send_key,
                args=(
                    eve_windows,
                    sleep_time,
                ),
            )
        else:
            self.sync_script_open = False
            messagebox.showwarning(
                "警告", "没有找到匹配窗口！\n请检查配置文件中的角色名，游戏角色是否登录"
            )
            print("没有找到匹配窗口")

    def send_key(self, eve_windows, sleep_time):
        """发送按键到匹配窗口"""
        send_key = self.settings.get_qb_send_key()
        for hwnd in eve_windows:
            send_key_to_eve_window(hwnd, send_key)
            print(f"发送按键到窗口: {hwnd}")
            time.sleep(sleep_time)

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
    def open_settings(self):
        """打开设置界面"""
        # 创建独立窗口
        settings_window = tk.Toplevel(self.preview_window)
        settings_window.title("配置管理")
        settings_window.geometry("550x650")
        settings_window.configure(bg="#2b2b2b")
        
        # 设置窗口属性
        settings_window.attributes("-topmost", True)  # 置顶
        settings_window.resizable(False, False)  # 固定大小
        
        try:
            # 初始化设置界面
            SettingsApp(settings_window)
        except Exception as e:
            print(f"初始化设置界面失败: {e}")
            messagebox.showerror("错误", f"无法打开设置界面: {str(e)}")
    
    def openUrl(self, url):
        """打开指定的URL"""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"无法打开链接: {e}")
            messagebox.showerror("错误", f"无法打开链接: {str(e)}")