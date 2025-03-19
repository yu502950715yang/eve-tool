# eve_tool eve 工具

# 功能

1.指定屏幕区域监控
需要监控的程序不能最小化

2.通过使用“·”快捷键实现快速点击切换到监控区域
快捷键在最小化的情况下也可以使用

3.多屏幕没测试 可能会有问题

# 使用方法

## <font color="red">拾取残骸需要自己按回车快速拾取！！！</font>
## <font color="red">拾取残骸需要自己按回车快速拾取！！！</font>
## <font color="red">拾取残骸需要自己按回车快速拾取！！！</font>

1.双击 eve_tool.exe文件启动程序

2.在屏幕上选取需要监控的区域

3.鼠标左键单击窗口中的位置鼠标会自动跳转到被监控区域对应的位置（鼠标自动移到被监控区域对应的位置并双击）

4.按键盘上“·”键鼠标会自动跳转到被监控区域中心位置（鼠标自动移到被监控区域中心位置并双击）

5.鼠标右键按住可以拖动窗口位置

6.鼠标右键双击窗口可以关闭程序

# 安装依赖

pip install -r requirements.txt

# 打包命令

pyinstaller --onefile --windowed --distpath ./dist --name eve_tool --icon ./images/icon.ico main.py 