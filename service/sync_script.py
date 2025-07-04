import time
import keyboard
from utils.settings import Settings
import pygetwindow as gw
import win32gui
import win32con
import win32process
import psutil


settings = Settings()
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
    patterns = settings.get_qb_settings().get("windows", [])
    # 移除空元素
    patterns = [pattern for pattern in patterns if pattern.strip()]
    if len(patterns) == 0:
        return []
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
    try: 
       return win32gui.GetWindowPlacement(hwnd)[1] == win32con.SW_SHOWMINIMIZED
    except Exception as e:
        print(f"获取窗口最小化状态失败: {e}")
        return False

def send_key_to_eve_window(hwnd, key):
    """发送按键到指定窗口"""
    key = key.lower()
    print(f"发送按键到窗口: {hwnd}, 按键: {key}")
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 如果窗口最小化，则恢复
        win32gui.SetForegroundWindow(hwnd)  # 将窗口带到前台
        time.sleep(0.05)
        keyboard.press_and_release(key)
    except Exception as e:
        print(f"发送按键失败: {e}")

def get_window_title(hwnds):
    """获取窗口标题"""
    windows_titles = []
    for hwnd in hwnds:
        try:
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows_titles.append(title)
        except Exception as e:
            print(f"获取窗口标题失败: {e}")
    return windows_titles