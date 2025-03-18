# eve_tool eve 工具

# 功能

1.指定屏幕区域监控
需要监控的程序不能最小化

2.通过使用“·”快捷键实现快速点击切换到监控区域
快捷键在最小化的情况下也可以使用

# 安装依赖

pip install -r requirements.txt

# 打包命令

pyinstaller --onefile --windowed --distpath ./dist --name eve_tool --icon ./images/icon.ico main.py 