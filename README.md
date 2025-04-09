# eve_tool eve 工具

# 功能

1.指定屏幕区域监控
需要监控的程序不能最小化

2.通过使用“·”快捷键实现快速点击切换到监控区域
快捷键在最小化的情况下也可以使用

3.预警功能
使用OpenCV对监控区域与预警图片进行匹配，如果匹配成功则发出警报

# 使用方法

## <font color="red">拾取残骸需要自己按回车快速拾取！！！</font>
## <font color="red">拾取残骸需要自己按回车快速拾取！！！</font>
## <font color="red">拾取残骸需要自己按回车快速拾取！！！</font>

1.双击 eve_tool.exe文件启动程序

2.在屏幕上选取需要监控的区域

3.鼠标左键拖动窗口位置

4.按键盘上“·”键鼠标会自动跳转到被监控区域中心位置（鼠标自动移到被监控区域中心位置并双击）

5.鼠标右键展示菜单栏

6.ctrl+alt+r 快捷键可以重新选取监控区域

7.ctrl+alt+1 开启预警功能 crtl+alt+2 关闭预警功能 (预警模板图片可以自定义，修改imgs/alert目录中的图片即可)

8.ctrl_alt+m 隐藏窗口 ctrl+alt+n 显示窗口

# 安装依赖

pip install -r requirements.txt

# 打包命令

运行 build.py 文件自动打包

# 配置文件说明
1.config.json 可自行修改
```json
{
    // 监控区域坐标 [左下角x,左下角y,右上角x,右上角y]
    "monitor_region": [ 0, 0, 0, 0],
    // 预警图片匹配阈值
    "enemy_match_threshold": 0.1,
    // 记录监控区域在屏幕上的坐标
    "windows_region": [0, 0]
}
```