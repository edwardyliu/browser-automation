# project/server/tasks/__init__.py

# === Import(s) ===
# => Local <=
from . import ina
from . import const
from . import utils

# === Export(s) ===
# => Tasks Module <=
def keys()->list:
    """Get a List of Available INA.Key Values

    Returns
    -------
    list
    """

    return const.TASKS_KEYS

def create_scan(raw:dict, uid:str=None, browser:str=None)->bool:
    """Create & Deploy an INA.Job Instance
    
    Custom Job: Scan

    Returns
    -------
    bool: Status
    """

    receipt:str = raw.get("receipt"); data:list = raw.get("data")
    if data:
        try:
            data.sort(key = lambda row: row.get("usrId") or "N/F")
            trues, falses = utils.partition(lambda row: row.get("orderId"), data)
            gets = map(
                lambda row: {
                    "lut": {**{
                        "usrId": row.get("usrId") or "N/A",
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

            handler = ina.Job(uid, browser=browser)
            for get in gets:
                lut = get["lut"]
                handler.push(const.TASK_GET_ORDER_BY_ID, elut = lut)
                
            prev_id = None
            for find in finds:
                lut = find["lut"]; curr_id = find["lut"]["usrId"]

                if prev_id != curr_id:
                    handler.push(const.TASK_SWAP_USER, elut = lut, trace = False)
                handler.push(const.TASK_FIND_ORDER, elut = lut)
                
                prev_id = curr_id
            handler.deploy(receipt)
            return True

        except KeyError: print(f"server.tasks.create_scan: Key Error - {raw}, {uid}")
    return False

def create_job(raw:dict, uid:str=None, browser:str=None)->bool:
    """Create & Deploy an INA.Job Instance
    
    Returns
    -------
    bool: Status
    """
    
    receipt:str = raw.get("receipt"); data:list = raw.get("data")
    if data:
        try:
            data = list( filter(lambda row: row.get("env") and row.get("name") and row.get("usrId"), data) )
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

            handler = ina.Job(uid, browser=browser); prev_id = None
            for task in tasks:
                key = ina.Key(task["env"], task["name"]); lut = task["lut"]
                task = const.TASKS_DICT.get(key); curr_id = lut["usrId"]
                
                if task:
                    if prev_id != curr_id:
                        handler.push(const.TASK_SWAP_USER, elut = lut, trace = False)
                    handler.push(task, elut = lut)
                
                prev_id = curr_id
            handler.deploy(receipt)
            return True

        except KeyError: print(f"server.tasks.create_job: Key Error - {raw}, {uid}")
    return False
