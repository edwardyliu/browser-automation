# project/server/tasks/tasks.py

# == Import(s) ==
# => Local
from . import ina
from . import const
from . import utils

# => System
import copy

# == Tasks API ==
def get_keys()->list:
    """Get a list of task key values

    Returns
    -------
    list: A list of task key values
    """

    return const.TASKKEYS

def create_scan(raw:dict, uid:str=None)->bool:
    """Create & deploy a scan instance

    Returns
    -------
    bool: Success or failure
    """

    receipt:str = raw.get("receipt"); data:list = raw.get("data")
    if data:
        try:
            data.sort(key = lambda row: row.get("usrId") or "N/F")
            trues, falses = utils.partition(lambda row: row.get("orderId"), data)
            gets = map(
                lambda row: {
                    "lut": {**{
                        "usrId": row.get("usrId") or "N/F",
                        "orderId": row["orderId"]
                    }, **(row["lut"] or {})}
                },
                trues
            )
            finds = map(
                lambda row: {
                    "lut": {**{
                        "usrId": row["usrId"],
                        "name": row["name"]
                    }, **(row["lut"] or {})}
                },
                falses
            )

            handler = ina.Job(uid)
            for get in gets:
                lut = get["lut"]
                handler.push(const.TASK_GETBYID, elut = lut)
                
            prev_id = None
            for find in finds:
                lut = find["lut"]; curr_id = find["lut"]["usrId"]

                if prev_id != curr_id:
                    handler.push(const.TASK_HOTSWAP, elut = lut, trace = False)
                handler.push(const.TASK_FINDBYORDER, elut = lut)
                
                prev_id = curr_id
            handler.deploy(receipt)
            return True

        except KeyError: print(f"server.tasks.create_scan: Key Error - {raw}")
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
            data = list( filter(lambda row: row.get("usrId"), data) )
            data.sort(key = lambda row: row["usrId"])
            tasks = map(
                lambda row: {
                    "env": row["env"],
                    "name": row["name"],
                    "lut": {**{
                        "usrId": row["usrId"]
                    }, **(row["lut"] or {})}
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

        except KeyError: print(f"server.tasks.create_job: Key Error - {raw}")
    return False
