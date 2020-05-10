# project/server/tasks/utils.py

# == Import(s) ==
# => Local
from . import config
from . import ina

# => System
import json
import logging
import datetime
from pathlib import Path
from collections import deque

# => External
import pytz

# == Utility Function(s) ==
# => Getter(s)
def timezone_converter_est(*args):
    """A timezone converter that converts from UTC to EST

    """

    utc_datetime = pytz.utc.localize(datetime.datetime.utcnow())
    est_timezone = pytz.timezone("US/Eastern")
    converted = utc_datetime.astimezone(est_timezone)
    return converted.timetuple()

def get_logger(uid:str)->logging.Logger:
    """Get logging object

    Parameters
    ----------
    uid: str
        The logger's UID

    Returns
    -------
    Logger: The logging object
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

def get_tasklist(log:logging.Logger=None, prefix:list=None, suffix:list=None)->list:
    """Get a list of task objects from "<basedir>/journal/.../*.json"

    Returns
    -------
    list: A list of task objects
    """

    tasks = []
    for filepath in list(Path(config.JOURNAL_DIRPATH).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"parsing task: {filepath}")
        task = parse_json(filepath)
        if task.key.env != "ALL":
            if prefix: task.extendleft(prefix)
            if suffix: task.extend(suffix)
            task.pushleft(ina.Command("printf", f"{task.key.env},{task.key.name}", None))

        tasks.append(task)
    
    return tasks

def get_taskdict(log:logging.Logger=None, prefix:list=None, suffix:list=None)->dict:
    """Get a list of task objects from "<basedir>/journal/.../*.json"

    Returns
    -------
    dict: A dictionary of task objects
    """
    
    tasks = {}
    for filepath in list(Path(config.JOURNAL_DIRPATH).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"parsing task: {filepath}")
        task = parse_json(filepath)
        if task.key.env != "ALL":
            if prefix: task.extendleft(prefix)
            if suffix: task.extend(suffix)
            task.pushleft(ina.Command("printf", f"{task.key.env},{task.key.name}", None))
        
        tasks[task.key] = task

    return tasks

# => Parser(s)
def parse_json(filepath:str)->ina.Task:
    """Parse JSON file into task object

    Parameters
    ----------
    filepath: str
        The JSON file path

    Returns
    -------
    model.Task: The task object
    """
    
    try:
        with open(filepath) as fp:
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
    
    except IndexError: raise IndexError(f"tasks.utils.parse_json: Index Error - {filepath}")
