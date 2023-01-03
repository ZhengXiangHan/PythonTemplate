# -*- coding: UTF-8 -*-
import sys, threading, time
from frame.debug import DEBUG_LEVEL, DebugPrint
from enum import unique, IntEnum # 整型数字枚举类
# 模组列表
ModuleList = []

@unique # 枚举类中key不能相同, 导入unique后, value也不能相同
class MODULESTATE(IntEnum):
    New = 0
    Initialized = 1
    End = 2
    def __lt__(self, other) -> bool:
        return self.value < other.value
    def __le__(self, other) -> bool:
        return self.value <= other.value
    def __gt__(self, other) -> bool:
        return self.value > other.value
    def __ge__(self, other) -> bool:
        return self.value >= other.value

class Module():
    '''模块类，功能都应该以模块为单位添加。
    
    先在文件开头创建模块类的实例，然后填入带return True/False的init_func/exit_func两个函数
    '''
    class ModuleThread(threading.Thread):
        def __init__(self, threadname:str, module, timesep:float=1):
            '''内部线程类，一个模块可以有多个线程，不应该让线程脱离于模块存在。使用时直接建实例并修改start_func、run_func、stop_func、pause_func、resume_func函数。这些函数默认为空。
        
            Args:
                threadname: 线程名
                module: 所属模块
                timesep: 运行中的每次执行run的时间间隔
            '''
            threading.Thread.__init__(self,name=threadname)
            self.threadname = threadname
            self.daemon = True
            self.__live = False
            self.start_func = self.__emptyF
            self.run_func = self.__emptyF
            self.stop_func = self.__emptyF
            self.pause_func = self.__emptyF
            self.resume_func = self.__emptyF
            self.timesep = timesep
            self.__pause_lock = threading.Lock()    # 用于暂停线程的线程锁
            self.module = module
            module.threadlist.append(self)
        # 重写run()方法
        def run(self):
            while self.module.getstate() != MODULESTATE.Initialized:
                pass
            self.__live = True
            self.start_func(self)
            while self.__live == True and self.module.getstate() != MODULESTATE.End:
                self.__pause_lock.acquire()    # 阻塞地获得锁
                # 日常运行
                self.run_func(self)
                self.__pause_lock.release()
                time.sleep(self.timesep)
        def __emptyF(self,threadself):
            pass
        def threadstart(self):
            self.start()
            self.join(timeout=0.1)
        def pause(self):
            while self.__pause_lock.acquire(blocking=False) == False:
                pass
            self.pause_func()
        def resume(self):
            if self.__live != False:
                self.resume_func(self)
                self.__pause_lock.release()   # 设置为True, 让线程继续
        def stop(self):
            if self.__live == True:
                self.__live = False
                self.stop_func(self)
        def isalive(self):
            return self.__live
    def __init__(self, module_name:str, init_dependent_list:list=[]):
        '''模块初始化方法'''
        self.module_name = module_name
        self.__state = MODULESTATE.New
        self.__debug = True
        # self.run_func = self._emptyF # 一次性处理的功能init即可完成，持续性处理推荐新建线程，否则这里就是主线程来执行，注意阻塞
        self.init_dependent_list = init_dependent_list    # 如['debug', 'xxxx'], 初始化依赖列表, 当模块初始化时, 要先初始化这里面的模块
        self.exit_dependent_list = []   # 退出依赖列表, 当模块退出时, 要先退出这里面的模块
        self.threadlist = []  # 模块线程列表
        global ModuleList
        ModuleList.append(self) # 加入模组列表
    def init_func(self):
        self.debuge_scs(self.module_name, "init.")
        return True
    def exit_func(self):
        self.debuge_scs(self.module_name, "exit.")
        return True
    # 模块Error打印
    def debuge_err(self, *values, file=sys.stdout, sep=' ', end='\n', flush=False, timeprint=True, newline=False):
        if self.__debug == True:
            DebugPrint('<',self.module_name,'>','[',threading.current_thread().name,']', *values, debug_level=DEBUG_LEVEL.Error, file=file, sep=sep, end=end, flush=flush, timeprint=timeprint, newline=newline)
    # 模块Warning打印
    def debuge_warn(self, *values, file=sys.stdout, sep=' ', end='\n', flush=False, timeprint=True, newline=False):
        if self.__debug == True:
            DebugPrint('<',self.module_name,'>','[',threading.current_thread().name,']', *values, debug_level=DEBUG_LEVEL.Warning, file=file, sep=sep, end=end, flush=flush, timeprint=timeprint, newline=newline)
    # 模块Info打印
    def debuge_info(self, *values, file=sys.stdout, sep=' ', end='\n', flush=False, timeprint=True, newline=False):
        if self.__debug == True:
            DebugPrint('<',self.module_name,'>','[',threading.current_thread().name,']', *values, debug_level=DEBUG_LEVEL.Info, file=file, sep=sep, end=end, flush=flush, timeprint=timeprint, newline=newline)
    # 模块Success打印
    def debuge_scs(self, *values, file=sys.stdout, sep=' ', end='\n',flush=False, timeprint=True, newline=False):
        if self.__debug == True:
            DebugPrint('<',self.module_name,'>','[',threading.current_thread().name,']', *values, debug_level=DEBUG_LEVEL.Success, file=file, sep=sep, end=end, flush=flush, timeprint=timeprint, newline=newline)
    # 模块debug状态切换
    def debugswitch(self):
        self.__debug = not self.__debug
    def getstate(self):
        return self.__state
    def _emptyF(self):
        return True
    def threadexit(self):
        for thread in self.threadlist:
            thread.stop()
    # 模块初始化, 在ModuleManagerInit中的依赖处理后才能使用
    def moduleinit(self)->bool:
        if self.__state != MODULESTATE.New:
            self.debuge_info("模块已完成初始化。")
            return True
        # print(self.module_name,self.init_dependent_list)
        for module in self.init_dependent_list:
            if module.getstate() == MODULESTATE.Initialized:
                continue
            if module.moduleinit() == False: # 深度遍历执行依赖模块的模块初始化
                self.debuge_err("依赖的模块:<",module.module_name,">初始化失败!")
                return False
        if self.__state == MODULESTATE.New and self.init_func() == False: # 自己的初始化函数
            self.debuge_err("模块初始化失败!")
            return False
        self.debuge_scs("模块初始化成功!")
        self.__state = MODULESTATE.Initialized
        return True
    # 模块退出, 在ModuleManagerExit中被调用
    def moduleexit(self)->bool:
        if self.__state == MODULESTATE.End:
            # self.debuge_info("模块不在运行状态。")
            return True
        elif self.__state == MODULESTATE.New:
            self.debuge_info("模块未初始化。")
            return True
        # print(self.module_name,self.exit_dependent_list)
        for module in self.exit_dependent_list:
            if module.getstate() == MODULESTATE.End:
                continue
            if module.moduleexit() == False:# 深度遍历执行依赖模块的模块退出
                self.debuge_warn("依赖的模块:<",module.module_name,">退出异常!")
        self.threadexit()
        if self.__state == MODULESTATE.Initialized and self.exit_func() == False:   # 自己的退出函数
            self.debuge_warn("模块退出异常!")
        self.__state = MODULESTATE.End
        self.debuge_scs("模块退出成功!")
        return True

def ModuleManagerInit():
    '''模块初始化'''
    global ModuleList
    # 模块依赖整理
    for module in ModuleList:
        # print("当前模块:",module.module_name)
        for i, module_name in enumerate(module.init_dependent_list, 0):  # 遍历依赖名称
            for dependentmodule in ModuleList:  # 遍历所有模块
                if module_name == dependentmodule.module_name:  # 对找到的依赖模块执行 字符串变引用操作
                    # print("对找到的依赖模块",module_name,"执行字符串变引用操作")
                    del module.init_dependent_list[i]
                    module.init_dependent_list.insert(i, dependentmodule)
                    dependentmodule.exit_dependent_list.append(module)  # 把该模块加入依赖模块的退出依赖列表
    for module in ModuleList:
        # print("管理器执行模块:",module.module_name,"的模块初始化")
        module.moduleinit()

def ModuleManagerExit():
    '''模块退出'''
    for module in ModuleList:
        module.moduleexit()

import atexit
# 程序退出
@atexit.register 
def clean():
    ModuleManagerExit()

def ShowAllThread():
    for module in ModuleList:
        DebugPrint("[",module.module_name,"]",end='')
        for thread in module.threadlist:
            DebugPrint("[",thread.threadname,":",thread.isalive(),"]")

def ShowAllModule():
    DebugPrint('RunningModule:',ModuleList)