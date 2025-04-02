from cmath import rect
from turtle import width
import win32gui


def get_window_rect(window_title):
    """获取指定窗口的坐标和尺寸"""
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        client_rect = win32gui.GetClientRect(hwnd)
        return {
            "left": rect[0],
            "top": rect[1],
            "width": rect[2] - rect[0],
            "height": rect[3] - rect[1],
            "client_width": client_rect[2],
            "client_height": client_rect[3],
        }
    else:
        return None
