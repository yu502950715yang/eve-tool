from ui.preview_window import PreviewWindow
from utils.screen_util import ScreenRegionSelector


def get_selected_region():
    """获取用户选择的屏幕区域，并启动预览窗口"""
    selector = ScreenRegionSelector()
    region = selector.select_region()
    if region:
        print(f"选中区域坐标: {region}")
        preview = PreviewWindow(region)
        preview.start()
    else:
        print("没有选择区域")
    return region


if __name__ == "__main__":
    selected_region = get_selected_region()
