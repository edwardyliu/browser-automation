# == Import(s) ==
# => Local
from . import config
from . import models

# => System
import os
import re
import json
import logging
import smtplib
import datetime
from pathlib import Path
from collections import deque
from email.message import EmailMessage

# => External
import pytz

# == Utility Function(s) ==
# => Logger
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
        The logger's ID

    Returns
    -------
    Logger:
        The logging object
    """

    log = logging.getLogger(uid)
    log.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fmt.converter = timezone_converter_est

    handle = logging.StreamHandler()
    handle.setLevel(logging.INFO)
    handle.setFormatter(fmt)

    log.addHandler(handle)
    return log

# => Parser
def parse_json(filepath:str)->models.Task:
    """Parse JSON file into a task object

    Parameters
    ----------
    filepath: str
        The JSON file path

    Returns
    -------
    model.Task: 
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
            
            cmds.append(models.Command(label, target, argv))
        return models.Task(models.Key(raw["name"], raw["env"]), cmds)
    
    except IndexError:
        raise IndexError(f"utils.parse_json: Index Error - {filepath}")

def parse_task(fmt:str, tbl:dict, results:dict)->str:
    """Parse job results into a formatted string

    Parameters
    ----------
    fmt: str
        The string format
    tbl: dict
        A lookup table
    results: dict
        The task's resulting lookup table 
    
    Returns
    -------
    str: The formatted string
    """

    for elem in re.findall(config.POSITIONAL, fmt):
        value = elem[2:-1]
        if value == config.TBLV: fmt = fmt.replace(elem, json.dumps(tbl))
        elif value == config.ARGV:
            span = []; result = results.get("${1}")
            while result:
                span.append(result)
                result = results.get("${" + str(len(span)+1) + "}")
            fmt = fmt.replace(elem, ", ".join(span))
        elif value.isdigit(): fmt = fmt.replace(elem, results.get(elem, "N/A"))
        else: fmt = fmt.replace(elem, tbl.get(value, "None"))
    return fmt

# => Getter
def next_cache_key(prefix:str, postfix:str)->str:
    """Get the next available '*.json' filepath

    Returns
    -------
    str: The cache filepath
    """

    filepath = os.path.join(config.DEFAULT_CACHE_DIRPATH, f"{prefix}1{postfix}")
    while os.path.isfile(filepath):
        pattern = re.findall(config.RE_NUMERAL, filepath)[0]
        filepath = filepath.replace(pattern, str(int(pattern)+1))
    return filepath

def get_tasks(log:logging.Logger=None)->list:
    """Get a list of task objects
    find all from "<basedir>/data/.../*.json"

    Returns
    -------
    list:
        A list of task objects
    """

    tasks = []
    for filepath in list(Path(config.DEFAULT_TASK_DIRPATH).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"parsing task: {filepath}")
        tasks.append(parse_json(filepath))
    return tasks

# => Functional
def cache(stdout:list)->str:
    """Cache the content of <stdout> into the next available '*.json' filepath
    
    Parameters
    ----------
    stdout: list
        A list of printf values

    Returns
    -------
    str: The cached filepath
    """

    filepath = next_cache_key("cache", ".json")
    with open(filepath, "w") as fp:
        json.dump(stdout, fp)
    return filepath

def load(filepath:str)->list:
    """Load the cached content from <filepath>
    
    Parameters
    ----------
    filepath: str
        A cached filepath

    Returns
    -------
    list: The cached content
    """
    
    with open(filepath, "r") as fp:
        stdout = json.load(fp)
    return stdout

# => Functional: E-mail
# TODO: create E-mail template & implement E-mail functionality
