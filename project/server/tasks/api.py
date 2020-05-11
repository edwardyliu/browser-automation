# project/server/tasks/api.py

# == Import(s) ==
# => Local
from . import ina
from . import const

# => System
import copy

# == Tasks API ==
def get_keys()->list:
    return const.TASKKEYS

def create_scan(raw:dict, uid:str=None)->bool:
    return False

def create_job(raw:dict, uid:str=None)->bool:
    """Create & deploy a job instance
    
    Returns
    -------
    bool: Success or failure
    """
    
    receipt:str = raw.get("receipt"); data:list = raw.get("data")
    if data:
        try:
            data.sort(key = lambda row: row["usrId"])
            tasks = map(
                lambda row: {
                    "env": row["env"],
                    "name": row["name"],
                    "lut": {**{
                        "usrId": row["usrId"]
                    }, **row["lut"]}
                },
                data
            )

            handler = ina.Job(uid); prev_id = None
            for task in tasks:
                key = ina.Key(task["env"], task["name"]); lut = task["lut"]
                task = const.TASKDICT.get(key); curr_id = lut["usrId"]

                if task:
                    if prev_id != curr_id:
                        handler.push(const.TASK_HOTSWAP, elut = lut, trace = False)
                    handler.push(task, elut = lut)
                
                prev_id = curr_id
            handler.deploy(receipt)
            return True

        except KeyError: pass
    return False
