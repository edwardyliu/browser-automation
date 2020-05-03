# project/server/tasks/service.py

# == Import(s) ==
# => Local
from . import ina

# == INA Service API ==
def exec_job(parcel:list, requestor:str=None):
    job = ina.Job()
    for item in parcel:
        key = ina.Key(item["env"], item["name"]); fmt = item.get("format"); lut = item.get("lut")
        job.push(key, fmt, lut)
    job.exec(requestor)

    return True
    