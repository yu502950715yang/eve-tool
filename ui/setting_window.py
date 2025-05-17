import tkinter as tk
from tkinter import ttk, messagebox
from utils.settings import Settings


class SettingsApp:
    def __init__(self, root):
        self.settings = Settings()
        self.root = root
        self.root.title("修改配置")
        self.root.geometry("400x400")
        # 设置根窗口背景为暗色
        self.root.configure(bg="#2b2b2b")
        # 初始化ttk样式，配置暗色与扁平化风格
        self.init_style()
        # 初始化UI组件
        self.create_widgets()
        # 加载当前配置
        self.load_config()

    def init_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#2b2b2b")
        style.configure("TLabel", background="#2b2b2b", foreground="white")
        style.configure("TNotebook", background="#2b2b2b")
        style.configure(
            "TNotebook.Tab", background="#3a3a3a", foreground="white", padding=5
        )
        style.map("TNotebook.Tab", background=[("selected", "#2b2b2b")])
        style.configure("TLabelframe", background="#2b2b2b", borderwidth=0)
        style.configure("TLabelframe.Label", background="#2b2b2b", foreground="white")
        style.configure(
            "TButton",
            background="#3a3a3a",
            foreground="white",
            relief="flat",
            borderwidth=0,
        )
        style.map("TButton", background=[("active", "#2b2b2b")])
        # 对Entry和Spinbox使用黑色背景与白色文字
        style.configure("TEntry", fieldbackground="#3a3a3a", foreground="white")
        style.configure("TSpinbox", fieldbackground="#3a3a3a", foreground="white")

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10, expand=True, fill="both")

        # 预警设置页面
        monitor_frame = ttk.Frame(notebook)
        notebook.add(monitor_frame, text="预警设置")

        # 匹配阈值
        threshold_frame = ttk.LabelFrame(monitor_frame, text="匹配设置")
        threshold_frame.pack(padx=5, pady=5, fill="x")

        ttk.Label(threshold_frame, text="敌方匹配阈值:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.threshold = ttk.Spinbox(
            threshold_frame,
            from_=0.1,
            to=1.0,
            increment=0.05,
            width=10,
            validate="key",
            validatecommand=(self.root.register(self.validate_threshold), "%P"),
        )
        self.threshold.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        # 新增提示标签
        ttk.Label(
            threshold_frame, 
            text="数值越小匹配越精确", 
            foreground="#888888",  # 灰色文字
            font=("Segoe UI", 8)    # 更小字号
        ).grid(
            row=0, column=2,
            padx=(0,5),  pady=5,
            sticky=tk.W
        )

        # QB设置页面
        qb_frame = ttk.Frame(notebook)
        notebook.add(qb_frame, text="QB设置")

        # QB基础设置
        qb_basic = ttk.LabelFrame(qb_frame, text="基本设置")
        qb_basic.pack(padx=5, pady=5, fill="x")

        ttk.Label(qb_basic, text="触发热键:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.qb_hotkey = ttk.Entry(qb_basic)
        self.qb_hotkey.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(qb_basic, text="执行按键:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.qb_sendkey = ttk.Entry(qb_basic)
        self.qb_sendkey.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(qb_basic, text="执行间隔(ms):").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.qb_delay = ttk.Spinbox(qb_basic, from_=50, to=5000, increment=50, width=10)
        self.qb_delay.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # 监控窗口列表
        window_list = ttk.LabelFrame(qb_frame, text="监控角色列表(每行一个)")
        window_list.pack(padx=5, pady=5, fill="both", expand=True)

        self.qb_windows = tk.Text(
            window_list,
            height=8,
            bg="#3a3a3a",
            fg="white",
            insertbackground="white",
            relief="flat",
        )
        self.qb_windows.pack(padx=5, pady=5, fill="both", expand=True)

        # 操作按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="保存配置", command=self.save_config).pack(
            side="right", padx=5
        )

    def load_config(self):
        """加载当前配置到界面"""
        # 匹配阈值
        self.threshold.delete(0, tk.END)
        self.threshold.insert(0, str(self.settings.get_enemy_match_threshold()))

        # QB设置
        qb = self.settings.get_qb_settings()
        self.qb_hotkey.delete(0, tk.END)
        self.qb_hotkey.insert(0, qb["triggerHotkey"])

        self.qb_sendkey.delete(0, tk.END)
        self.qb_sendkey.insert(0, qb["sendKey"])

        self.qb_delay.delete(0, tk.END)
        self.qb_delay.insert(0, str(qb["delayBetween"]))

        self.qb_windows.delete("1.0", tk.END)
        self.qb_windows.insert("1.0", "\n".join(qb["windows"]))

    def save_config(self):
        """保存配置"""
        try:
            # 收集表单数据
            new_settings = {
                "enemy_match_threshold": float(self.threshold.get()),
                "qb": {
                    "triggerHotkey": self.qb_hotkey.get(),
                    "sendKey": self.qb_sendkey.get(),
                    "delayBetween": int(self.qb_delay.get()),
                    "windows": self.qb_windows.get("1.0", tk.END).strip().split("\n"),
                },
            }

            # 更新配置
            self.settings.settings = self.settings.merge_settings_with_defaults(
                new_settings
            )
            self.settings._save_settings()

            messagebox.showinfo("成功", "配置保存成功！")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {str(e)}")
            
    def validate_threshold(self, proposed_value):
        if proposed_value == "":
            return True  # 允许为空，方便输入过程
        try:
            value = float(proposed_value)
            return 0 <= value <= 1.0
        except ValueError:
            return False
