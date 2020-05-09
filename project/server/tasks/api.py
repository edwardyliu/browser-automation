# project/server/tasks/api.py

# == Import(s) ==
# => Local
from . import ina
from . import constant

# == INA API ==
def get_task_keys()->list:
    return constant.TASK_KEYS

def create_job(message:dict, uid:str=None):
    receipt:str = message.get("receipt"); tasks:dict = message.get("tasks")
    if tasks:
        try:
            job = ina.Job(uid)
            for task in tasks:
                key = ina.Key(task["env"], task["name"]); fmt = task.get("fmt"); lut = task.get("lut")
                task = constant.TASK_DICT.get(key)
                if task: job.push(task, fmt, lut)
            job.exec(receipt)
            return True
        except KeyError: pass
    return False
    