# -*- coding: UTF-8 -*-
import os
os.environ['WORKON_HOME'] = "D:\WorkSpace\PythonTemplate"
import sys
from frame.debug import my_excepthook
sys.excepthook = my_excepthook # 未知异常中断处理
from frame.internation import _ # frame.internation是自动创建翻译文件的识别标志
from frame.modulemanager import ModuleManagerInit, ModuleManagerExit

import atexit
# 程序退出
@atexit.register 
def clean():
    ModuleManagerExit()

# 以上是预处理，例如确认执行路径，文件存放位置，这里面才是正式开始
if __name__ == "__main__":
    # import frame.config
    # frame.config.Write("one.ini", "default", "hhh", "1")
    # print(frame.config.Read("one.ini", "default", "hhh"))
    # import new.new2
    ModuleManagerInit()
    print(_("hello world"))
    while True:
        cmd = input("请输入:")
        if cmd == "c":
            break
    ModuleManagerExit()
    input()