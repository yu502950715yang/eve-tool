from ui.preview_window import PreviewWindow
from ui.screen_region_selector import ScreenRegionSelector
from utils.settings import Settings

settings = Settings()


def get_selected_region(window_region=None, fist_run=True):
    """获取用户选择的屏幕区域，并启动预览窗口"""
    region = None
    if fist_run:
        print("第一次运行，请选择监控区域")
        monitor_region = settings.get_monitor_region()
        print(f"配置文件中的监控区域: {monitor_region}")
        # 判断监控区域的4个坐标是否都为0，如果都为0，则重新选择监控区域
        if (
            monitor_region
            and monitor_region[0] == 0
            and monitor_region[1] == 0
            and monitor_region[2] == 0
            and monitor_region[3] == 0
        ):
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
        print("没有选择区域")

def select_region():
    """选择屏幕区域"""
    selector = ScreenRegionSelector()
    region = selector.select_region()
    settings.save_monitor_region(region)
    return region


def restart_preview(window_region):
    """重新选择监控区域"""
    print("重新选择区域")
    get_selected_region(window_region, False)


if __name__ == "__main__":
    get_selected_region()
