# project/server/tasks/api.py

# == Import(s) ==
# => Local
from . import ina

# == INA API ==
def create_task(message:dict, uid:str=None):
    receiver:str = message.get("receiver"); parcel:dict = message.get("parcel")
    if parcel:
        try:
            job = ina.Job(uid)
            for item in parcel:
                key = ina.Key(item["env"], item["name"]); fmt = item.get("fmt"); lut = item.get("lut")
                job.push(key, fmt, lut)
            job.exec(receiver)
            return True
        except KeyError: pass
    return False
    