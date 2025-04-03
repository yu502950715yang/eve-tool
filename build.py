# build.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onedir',
    '--windowed',
    '--distpath=./dist',
    '--name=eve_tool',
    '--icon=./imgs/icon.ico',
    '--add-data=imgs/*;imgs',
    '--add-data=sounds/*;sounds',
    '--add-data=config/*;config'
])