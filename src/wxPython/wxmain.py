# -*- coding: UTF-8 -*-
import wx, win32api, sys, os
import wx.lib.agw.aui as aui
APP_TITLE = os.environ['PROJECT_NAME']
APP_ICON = os.environ['WORKON_HOME']+'\\res\\template.ico' # 请更换成你的icon

class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''
    id_open = wx.NewId()
    id_save = wx.NewId()
    id_quit = wx.NewId()
    id_help = wx.NewId()
    id_about = wx.NewId()
    def __init__(self):
        '''构造函数'''
        wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        # 默认style是下列项的组合：wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN 
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 600))
        self.Center()
        # 以下代码处理图标
        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else :
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        # 以下可以添加各类控件
        pass
        
class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame()
        self.Frame.Show()
        return True

def beginApp():
    app = mainApp(redirect=True, filename="wxdebug.txt")
    app.MainLoop()

# 模块管理
from frame.modulemanager import Module
module_new = Module("wxPython", init_dependent_list=[])
