# -*- coding: utf-8 -*- 
import os, gettext, sys

# 在其他文件中导入时, frame.internation是自动创建翻译文件的识别标志

Language_List = ["zh-CN", "en-US"]
# 语言, 默认中文
Language = "zh-CN"

def changeLanguage(lang:str):
    if type(lang) != str:
        return False
    if lang not in Language_List:
        return False
    currentDir = os.environ["WORKON_HOME"]+"\i18n"
    gettext.translation(domain='resource', localedir=currentDir, languages=[lang]).install(True)
    return True

# Get loc string by language
def getLocStrings():
    currentDir = os.environ["WORKON_HOME"]+"\i18n"
    return gettext.translation(domain='resource', localedir=currentDir, languages=[Language, "en-US"]).gettext 

_ = getLocStrings()
