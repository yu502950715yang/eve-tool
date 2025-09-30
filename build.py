from pickle import BUILD
import PyInstaller.__main__
import shutil
import os

BUILD_PATH = "dist/eve_tool"

# 清理历史构建
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

PyInstaller.__main__.run(
    [
        "main.py",
        "--onedir",
        "--windowed", # 隐藏控制台
        "--distpath=./dist",
        "--name=eve_tool",
        "--icon=./imgs/icon.ico",
        "--hidden-import=pyautogui",
        # "--strip",  # 去除调试信息 windows会报错
        "--runtime-hook=runtime_hook.py",  # 自定义 hook
    ]
)


# 打包完成后复制资源文件夹到dist目录
def copy_resources():
    resources = ["imgs", "sounds"]  # 需要复制的文件夹列表
    dist_path = os.path.abspath(BUILD_PATH)  # 获取打包目录绝对路径

    for folder in resources:
        src = os.path.abspath(folder)  # 源文件夹路径
        dst = os.path.join(dist_path, folder)  # 目标路径（打包目录下）

        # 如果目标已存在则先删除（避免冲突）
        if os.path.exists(dst):
            shutil.rmtree(dst)
        # 复制文件夹
        shutil.copytree(src, dst)
        print(f"[SUCCESS] 已复制: {folder} -> {dst}")


# 执行复制操作
copy_resources()
