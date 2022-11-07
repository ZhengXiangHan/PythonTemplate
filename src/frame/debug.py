# -*- coding: UTF-8 -*-
import sys, datetime, time, os
from enum import unique, IntEnum # 整型数字枚举类

@unique # 枚举类中key不能相同, 导入unique后, value也不能相同
class DEBUG_LEVEL(IntEnum):
    Error = 0
    Warning = 1
    Success = 2
    Info = 3

# debug等级, 小于等于这个等级的才会显示
Debug_Level = DEBUG_LEVEL.Info

# 调试打印
def DebugPrint(*values, debug_level=DEBUG_LEVEL.Info, file=sys.stdout, sep=' ', end='\n', flush=False, timeprint=True, newline=False):
    '''若满足Debug级别条件，则将值打印到流或sys的调试区域。可选关键字参数：

    debug_level: 该次打印所属的debug等级
    file: 类似文件的对象（流），默认为当前sys.stdout。
    sep: 插入值之间的字符串，默认为空格。
    end : 最后一个值后附加的字符串，默认为换行符。
    flush: 是否强制刷新流。
    timeprint: 是否打印时间
    newline: 是否新起一行
    '''
    if Debug_Level.value < debug_level.value:
        return
    if newline == True: # 新起一行
        print('')
    # 3.10之前的版本使用threading.currentThread().getName() , thread_name=True 线程部分放到threadmanager
    # tname = threading.current_thread().name # 线程名
    # if thread_name == True:
    #     print("[" + tname + "]", end='')
    if timeprint == True:       #打印时间，时:分:秒.微秒
        print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f') + "]",*values, file=file, sep=sep, end=end, flush=flush)
    else:
        print(*values, file=file, sep=sep, end=end, flush=flush)

# # 在框中打印, 有bug
# def print_in_frame(title:str, body:str, lefttop="╔", righttop="╗", leftbottom="╚", rightbottom="╝", horizontal="═", 
# Vertical="║"):
#     width = os.get_terminal_size().columns - 5
#     Vertical_len = len(Vertical)
#     print(lefttop, "".center(width, horizontal), righttop)  # 顶部
#     print(Vertical, title.center(width - len(title), " "), Vertical) # 标题
#     for line in body.splitlines(keepends=False):
#         while len(line) >= 0:
#             if len(line) > width:
#                 print(Vertical, line[:width - Vertical_len].ljust(width, " "), Vertical) # 内容
#                 line = line[width - 1:]
#             else:
#                 print(Vertical, line.ljust(width, " "), Vertical) # 内容
#                 break
#     print(leftbottom, "".center(width, horizontal), rightbottom)  # 底部

# # 带前缀的print
# def print_with_prefix(*values, end='\n', file=sys.stdout, flush=False):
#     print(config.Cmd_dict['menu_prefix'], *values, end=end, file=file, flush=flush)

# 重写my_excepthook, 对于没有被捕获的异常, python统一用 sys.excepthook 这个函数来处理, 发生异常时, 程序中断并输出很多异常信息。
def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += ' File "%.500s", line %d, in %.500s\n' % (filename, lineno, name)
        tb = tb.tb_next
    msg += ' %s: %s\n' %(exc_type.__name__, exc_value)
    print(str(datetime.datetime.now().month)+ '月' + str(datetime.datetime.now().day) + '日 ' + datetime.datetime.now().strftime('%H:%M:%S.%f') + '\n' + msg, file=open(os.environ["WORKON_HOME"]+'\error.log','a+'))
    DebugPrint("出现未处理异常, 您可以查看error.log并联系作者。", debug_level=DEBUG_LEVEL.Error)

# 延迟
def Delay(second:int):
    time.sleep(second)
