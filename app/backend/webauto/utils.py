# == Import(s) ==
# => Local
from . import config
from . import models

# => System
import datetime
import logging
import json
import os
import re
from collections import deque
from pathlib import Path

# => External
import pytz
from selenium import webdriver

# == Utility Function(s) ==
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

def get_webdriver()->webdriver:
    """Get selenium webdriver: geckodriver

    """

    options = webdriver.FirefoxOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(executable_path=config.DEFAULT_DRIVER_EXEPATH, options=options)
    driver.maximize_window()
    return driver

def next_key(prefix:str, postfix:str)->str:
    """Get the next available '*.json' filepath

    Returns
    -------
    str: The cache filepath
    """

    filepath = os.path.join(config.DEFAULT_CACHE_DIRPATH, f"{prefix}1{postfix}")
    while os.path.isfile(filepath):
        pattern = re.findall(config.RE_NUMERAL_DOT_JSON, filepath)[0]
        filepath = filepath.replace(pattern, str(int(pattern)+1))
    return filepath

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

    filepath = next_key("cache", ".json")
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

def parse_json_file(filepath:str)->models.Sequence:
    """Parse the JSON file into a sequence model

    Parameters
    ----------
    filepath: str
        The JSON file path

    Returns
    -------
    model.Sequence: 
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
        return models.Sequence(raw["name"], raw["env"], cmds)
    
    except IndexError:
        raise IndexError(f"utils.parse_json_file: Index Error - {filepath}")
    
    except Exception:
        raise IndexError(f"utils.parse_json_file: Invalid JSON - {filepath}")

def get_sequences(log:logging.Logger=None)->list:
    """Get a list of sequence models
    find all from "<basedir>/data/.../*.json"

    Returns
    -------
    list:
        A list of sequence models
    """

    sequences = []
    for filepath in list(Path(config.DEFAULT_SEQUENCE_DIRPATH).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"build sequence: {filepath}")
        sequences.append(parse_json_file(filepath))
    return sequences

def parse_job(fmt:str, argv:dict, results:dict)->str:
    """Parse job results into formatted string

    Parameters
    ----------
    fmt: str
        The string format
    argv: dict
        A lookup table
    results: dict
        The sequence's stdout lookup table 
    
    Returns
    -------
    str: The formatted string
    """

    for elem in re.findall(config.POSITIONAL, fmt):
        value = elem[2:-1]
        if value == "@RESULT":
            span = []; result = results.get("${1}")
            while result:
                span.append(result)
                result = results.get("${" + str(len(span)+1) + "}")
            fmt = fmt.replace(elem, ", ".join(span))
        elif value.isdigit(): fmt = fmt.replace(elem, results.get(elem, "N/A"))
        elif value == "@": fmt = fmt.replace(elem, json.dumps(argv))
        else: fmt = fmt.replace(elem, argv.get(value, "None"))
    return fmt
