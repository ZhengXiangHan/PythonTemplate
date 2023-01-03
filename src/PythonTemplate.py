# -*- coding: UTF-8 -*-
import os, sys
os.environ['PROJECT_NAME'] = "PythonTemplate"
os.environ['WORKON_HOME'] = "D:\WorkSpace\\" + os.environ['PROJECT_NAME']
import frame.config, frame.debug, frame.internation, frame.modulemanager
from frame.internation import _ # frame.internation是自动创建翻译文件的识别标志
from frame.modulemanager import ModuleManagerInit, ModuleManagerExit, ShowAllModule
# import wxPython.wxmain
# 以上是预处理，例如确认执行路径，文件存放位置，这里面才是正式开始
if __name__ == "__main__":
    # import frame.config
    # if frame.config.Write("default.ini", "default", "hhh", "1") == True:
    #     frame.config.ShowCash()
    #     print('hhh=',frame.config.Read("default.ini", "default", "hhh"))
    #     frame.config.ShowCash()
    #     print('[default]=',frame.config.Read("default.ini", "default"))
    #     frame.config.ShowCash()
    # import new.new2
    ModuleManagerInit()
    # ShowAllModule()
    # wxPython.wxmain.beginApp()
    # print(_("hello world"))
    # while True:
    #     cmd = input("请输入:")
    #     if cmd == "c":
    #         break
