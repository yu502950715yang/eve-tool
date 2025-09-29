import time
import keyboard
from utils.settings import Settings
import pygetwindow as gw
import win32api
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

def send_key_to_eve_window_background(hwnd, key):
    """在后台发送按键到指定窗口，不改变窗口焦点"""
    key = key.upper()  # 转换为大写以便匹配
    print(f"后台发送按键到窗口: {hwnd}, 按键: {key}")
    
    try:
        # 处理功能键
        if key.startswith('F') and len(key) > 1:
            # 处理 F1-F12 功能键
            try:
                f_number = int(key[1:])
                if 1 <= f_number <= 12:
                    vk_code = getattr(win32con, f'VK_F{f_number}')
                else:
                    print(f"不支持的功能键: {key}")
                    return
            except ValueError:
                print(f"无效的功能键格式: {key}")
                return
        else:
            # 处理普通字符键
            key = key.lower()
            vk_code = win32api.VkKeyScan(key)
            if vk_code == -1:
                print(f"无法找到键码: {key}")
                return
            vk_code = vk_code & 0xFF
            
        scan_code = win32api.MapVirtualKey(vk_code, 0)
        
        # 发送按键按下消息
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 
                           (scan_code << 16) | 0x00000001)
        time.sleep(0.01)
        
        # 发送按键释放消息
        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 
                           (scan_code << 16) | 0xC0000001)
                           
    except Exception as e:
        print(f"后台发送按键失败: {e}")

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