import time

import keyboard
from utils.settings import Settings
import pygetwindow as gw
import win32gui
import win32con
import win32process
import psutil


settings = Settings()

# 同步脚本配置
sync_script_config = settings.get_qb_settings()

def get_process_name(hwnd):
    """获取窗口进程名"""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return psutil.Process(pid).name()
    except Exception:
        return None

def get_matched_windows():
    """获取匹配窗口"""
    windows = []
    patterns = sync_script_config.get("windows", [])
    for win in gw.getAllWindows():
        hwnd = win._hWnd
        title = win.title
        exe_name = get_process_name(hwnd)
        
        for pattern in patterns:
            if pattern in title or (exe_name and pattern in exe_name):
                windows.append(hwnd)
                break
    return windows

def is_minimized(hwnd):
    """检查窗口是否最小化"""
    return win32gui.GetWindowPlacement(hwnd)[1] == win32con.SW_SHOWMINIMIZED

def send_key_to_eve_window(hwnd, key, require_activate):
    """发送按键到指定窗口"""
    key = key.lower()
    
    if require_activate:
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 如果窗口最小化，则恢复
            win32gui.SetForegroundWindow(hwnd)  # 将窗口带到前台
            time.sleep(0.1)
            keyboard.press_and_release(key)
        except Exception as e:
            print(f"发送按键失败: {e}")
    else:
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
        time.sleep(0.05)
        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, key, 0)