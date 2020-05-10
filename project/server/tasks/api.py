# project/server/tasks/api.py

# == Import(s) ==
# => Local
from . import ina
from . import constant

# => System
import copy

# == INA API ==
def get_keys()->list:
    return constant.TASK_KEYS

def create_job(tasks:list, receipt:str=None, uid:str=None):
    try:
        job = ina.Job(uid)

        prev = None
        for task in tasks:
            key = ina.Key(task["env"], task["name"]); fmt = task.get("fmt"); lut = task.get("lut")
            task = constant.TASK_DICT.get(key); curr = lut.get("usrId")
            if task: 
                if curr != prev: 
                    task = copy.deepcopy(task)
                    task = task.extendleft(constant.TASK_SWITCH.cmds)
                job.push(task, fmt, lut)
            prev = curr
        
        job.exec(receipt)
        return True
    
    except KeyError: return False
    