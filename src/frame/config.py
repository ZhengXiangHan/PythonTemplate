# -*- coding: UTF-8 -*-
import configparser, os
from frame.debug import DebugError

# 这个相当于要靠临时环境变量来确定程序的安装位置，然后在安装位置根目录下\config
Config_Path = os.environ["WORKON_HOME"]+"\\config\\"

def eval_dict(dict:dict):
    '''把字典中每个键对应的值都eval一遍'''
    for key in dict.keys():
        dict[key] = eval(dict[key])
    return dict

def ReadFile(ConfigFile:str, encoding='utf-8'):
    '''读取并解析文件名或可迭代文件名。
    
    无法打开的文件将被默认忽略；这样设计的目的是，您可以指定一个可迭代的潜在配置文件位置（例如，当前目录、用户的主目录、系统范围目录），并将读取可迭代中的所有现有配置文件。也可以给出单个文件名。

    返回成功读取文件的列表。
    '''
    config = configparser.ConfigParser()    # 创建配置文件对象
    config.read(ConfigFile, encoding)       # 读取文件
    return config

def Read(ConfigFile:str, section:str, key:str='', encoding='utf-8'):
    '''读取配置文件，可以获取整个分组字典，也可以获取其中的某个值'''
    config = ReadFile(Config_Path+ConfigFile, encoding)
    if section not in config.sections():
        raise DebugError(section+"分组未找到。")
    if key != '':
        if key not in config.options(section):
            raise DebugError(key+"key未找到。")
        return eval(config.get(section, key))   # 获取单个值
    return eval_dict(dict(config.items(section)))  # 通过dict方法把section分组的内容转换为字典

def Write(ConfigFile:str, section:str, key:str, value:str, encoding='utf-8'):
    '''写入配置文件'''
    config = ReadFile(Config_Path+ConfigFile, encoding)
    if section not in config.sections():
        config.add_section(section)
    config.set(section, key, value)
    config.write(open(Config_Path+ConfigFile, "w"))
