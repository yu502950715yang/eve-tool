import time

import pyautogui

from utils.screen_util import get_selected_region


# 定义拾取残骸的函数
def loot_wrecks():
    # 模拟按下Alt键
    pyautogui.keyDown('alt')
    time.sleep(0.1)

    # 模拟按下L键（假设L键是拾取残骸的快捷键）
    pyautogui.press('l')
    time.sleep(0.1)

    # 松开Alt键
    pyautogui.keyUp('alt')
    time.sleep(0.1)


# 主循环，持续检测并拾取残骸
def main():
    # 调用屏幕选择器获取当前选中区域的坐标
    selected_region = get_selected_region()

    if not selected_region:
        print("No region selected. Exiting.")
        return

    while True:
        # 检测2500米范围内的残骸（假设这里有一个检测函数）
        if detect_wrecks_within_2500m():
            loot_wrecks()
        time.sleep(1)  # 每1秒检测一次


# 假设的检测函数，实际需要根据EVE的API或屏幕识别来实现
def detect_wrecks_within_2500m():
    # 这里可以添加检测逻辑，例如通过EVE的API获取残骸位置信息
    # 或者通过屏幕识别技术来检测残骸
    return True  # 假设始终有残骸


if __name__ == "__main__":
    main()
