from tkinter import messagebox
from ui.preview_window import PreviewWindow
from ui.screen_region_selector import ScreenRegionSelector
from utils.settings import Settings

settings = Settings()

def is_region_empty(region):
    """判断区域是否为空"""
    return region is None or all(coord == 0 for coord in region)

def terminate_with_message(message):
    """显示消息并终止程序"""
    messagebox.showwarning("警告", message)
    raise SystemExit(0)

def get_selected_region(window_region=None, first_run=True):
    """获取用户选择的屏幕区域，并启动预览窗口
    Args:
        window_region: 窗口区域，重新选择区域时使用，默认为None
        first_run: 是否是第一次运行，如果是第一次运行，则从配置文件中读取监控区域
    """
    region = None
    if first_run:
        print("第一次运行，请选择监控区域")
        monitor_region = settings.get_monitor_region()
        print(f"配置文件中的监控区域: {monitor_region}")
        # 判断监控区域的4个坐标是否都为0，如果都为0，则重新选择监控区域
        if is_region_empty(monitor_region):
            print("配置文件中的监控区域为0，请重新选择监控区域")
            region = select_region()
        else:
            region = monitor_region
    else:
        region = select_region()
    if region:
        print(f"选中区域坐标: {region}")
        preview = PreviewWindow(region, restart_preview, window_region)
        preview.start()
    else:
        terminate_with_message("未选择监控区域，程序将退出！")


def select_region():
    """选择屏幕区域"""
    selector = ScreenRegionSelector()
    region = selector.select_region()
    print(f"选择的区域: {region}")
    if region is not None:
        settings.save_monitor_region(region)
    else :
        region = settings.get_monitor_region()
        if is_region_empty(region):
            messagebox.showwarning("未选择监控区域", "未选择监控区域，程序将退出！")
            exit(0)
    return region


def restart_preview(window_region):
    """重新选择监控区域
    Args:
        window_region: 窗口所在区域
    """
    get_selected_region(window_region, False)


if __name__ == "__main__":
    window_region = settings.get_windows_region()
    get_selected_region(window_region=window_region)
