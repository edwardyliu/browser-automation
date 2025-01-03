# project/server/tasks/utils.py

# === Import(s) ===
# => Local <=
from . import ina
from . import config

# => System <=
import json
import logging
import datetime
from pathlib import Path
from collections import deque
from itertools import filterfalse, tee

# => External <=
import pytz

# === Utility Function(s) ===
# => Converter(s) <=
def timezone_converter_est(*args):
    """A timezone converter: from UTC to EST

    """

    utc_datetime = pytz.utc.localize(datetime.datetime.utcnow())
    est_timezone = pytz.timezone("US/Eastern")
    converted = utc_datetime.astimezone(est_timezone)
    return converted.timetuple()

# => Getter(s) <=
def get_logger(uid:str)->logging.Logger:
    """Get a Logger object

    Parameters
    ----------
    uid: str
        A UID for the Logger object

    Returns
    -------
    Logger
    """

    log = logging.getLogger(uid)
    log.setLevel(config.LOG_LEVEL)

    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fmt.converter = timezone_converter_est

    handle = logging.StreamHandler()
    handle.setLevel(config.LOG_LEVEL)
    handle.setFormatter(fmt)
    log.addHandler(handle)
    return log

def get_task_list(log:logging.Logger=None, prefix:list=None, suffix:list=None)->list:
    """Get 'list' of Task Objects via JSONs from "journal/*.json"

    Returns
    -------
    list
    """

    tasks = []
    for jsonpath in list(Path(config.PATH_JOURNAL).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"parsing task: {jsonpath}")
        task = json2task(jsonpath)
        if task.key.env != config.DEFAULT_NA:
            if prefix: task.extendleft(prefix)
            if suffix: task.extend(suffix)
        task.pushleft(ina.Command("printf", f"{task.key.env},{task.key.name}", None))

        tasks.append(task)
    return tasks

def get_task_dict(log:logging.Logger=None, prefix:list=None, suffix:list=None)->dict:
    """Get 'dict' of Task Objects via JSONs from "journal/*.json"
    
    Keys are their respective INA.Key objects

    Returns
    -------
    dict
    """
    
    tasks = {}
    for jsonpath in list(Path(config.PATH_JOURNAL).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"parsing task: {jsonpath}")
        task = json2task(jsonpath)
        if task.key.env != config.DEFAULT_NA:
            if prefix: task.extendleft(prefix)
            if suffix: task.extend(suffix)
        task.pushleft(ina.Command("printf", f"{task.key.env},{task.key.name}", None))
        
        tasks[task.key] = task
    return tasks

def get_tupled_task_dict(log:logging.Logger=None, prefix:list=None, suffix:list=None)->dict:
    """Get 'dict' of Task Objects via JSONs from "journal/*.json"
    
    Keys are tuple2s of INA.Key.env & INA.Key.name
    
    Returns
    -------
    dict
    """

    tasks = {}
    for jsonpath in list(Path(config.PATH_JOURNAL).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"parsing task: {jsonpath}")
        task = json2task(jsonpath)
        if task.key.env != config.DEFAULT_NA:
            if prefix: task.extendleft(prefix)
            if suffix: task.extend(suffix)
        task.pushleft(ina.Command("printf", f"{task.key.env},{task.key.name}", None))
        
        tasks[(task.key.env, task.key.name)] = task
    return tasks

# => Parser(s) <=
def json2task(jsonpath:str)->ina.Task:
    """Construct an INA Task Object via JSON

    Required JSON Format:
    {
        "name": <INA.Key.name>
        "env: <INA.Key.env>
        "commands": [
            [<INA.Command.label>, {
                "target": <INA.Command.target>,
                "argv": <INA.Command.argv>
            }], 
            
            ...
        ]
    }

    Parameters
    ----------
    jsonpath: str
        The JSON file path

    Returns
    -------
    Task
    """
    
    try:
        with open(jsonpath) as fp:
            raw = json.load(fp)
        
        cmds = deque([])
        for cmd in raw["commands"]:
            label = cmd[0].lower() # possible index error
            target = None
            argv = None

            if len(cmd) > 1:
                if isinstance(cmd[1], dict): 
                    target = cmd[1].get("target", None)
                    argv = cmd[1].get("argv", None)
                    if argv and not isinstance(argv, list): argv = [argv]
                else: target = cmd[1]
            
            cmds.append(ina.Command(label, target, argv))
        return ina.Task(ina.Key(raw["env"], raw["name"]), cmds)
    
    except IndexError: raise IndexError(f"server.tasks.json2task: Index Error - {jsonpath}")

def partition(pred, iterable):
    """Use a predicate to partition entries into true entries and false entries

    Parameters
    ----------
    pred: func
        The predicate function
    iterable: iter
        An iterator object
    
    Returns
    -------
    A tuple2, both are iterators: trues, falses
    """

    t1, t2 = tee(iterable)
    return filter(pred, t1), filterfalse(pred, t2)
