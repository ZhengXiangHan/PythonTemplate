# -*- coding: UTF-8 -*-
from frame.modulemanager import Module

module_new = Module("module_new1", init_dependent_list=[])
def initF():
    module_new.debuge_scs(module_new.module_name, "init.")
    return True
def exitF():
    module_new.debuge_scs(module_new.module_name, "exit.")
    return True
module_new.init_func=initF
module_new.exit_func=exitF

thread = Module.ModuleThread("new1_thread", module_new)
def startT():
    module_new.debuge_info(thread.threadname, "start.")
def runT():
    module_new.debuge_info(thread.threadname, "run.")
def stopT():
    module_new.debuge_info(thread.threadname, "stop.")
def pauseT():
    module_new.debuge_info(thread.threadname, "pause.")
def resumeT():
    module_new.debuge_info(thread.threadname, "resume.")
thread.start_func=startT
thread.run_func=runT
thread.stop_func=stopT
thread.pause_func=pauseT
thread.resume_func=resumeT
thread.threadstart()