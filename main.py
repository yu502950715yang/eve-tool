from ui.preview_window import PreviewWindow
from ui.screen_region_selector import ScreenRegionSelector


def get_selected_region(window_region=None):
    """获取用户选择的屏幕区域，并启动预览窗口"""
    selector = ScreenRegionSelector()
    region = selector.select_region()
    if region:
        print(f"选中区域坐标: {region}")
        preview = PreviewWindow(region, restart_preview, window_region)
        preview.start()
    else:
        print("没有选择区域")


def restart_preview(window_region):
    """重新选择监控区域"""
    print("重新选择区域")
    get_selected_region(window_region)


if __name__ == "__main__":
    get_selected_region()
