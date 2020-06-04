# project/server/tasks/ina/utils.py

# === Import(s) ===
# => Local <=
from . import const
from . import config

# => System <=
import os
import re
import json
import logging
import datetime

# => External <=
import pytz
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

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

def cache_key(prefix:str, postfix:str)->str:
    """Get next available file path of the format: <prefix>r"([0-9]+)"<postfix>
    Starting with the numerical number of '1'

    Parameters
    ----------
    prefix: str
        The prefix string
    postfix: str
        The postfix string

    Returns
    -------
    str
    """

    path = os.path.join(config.PATH_CACHE, f"{prefix}1{postfix}")
    while os.path.isfile(path):
        pattern = re.findall(const.RE_NUMERAL, path)[0]
        path = path.replace(pattern, str(int(pattern)+1))
    return path

# => Functional <=
def cache(results:list)->str:
    """Cache content of <results>
    
    Parameters
    ----------
    results: list
        A list of printf statements

    Returns
    -------
    str: The file path
    """

    path = cache_key("cache", ".json")
    with open(path, "w") as fp:
        json.dump(results, fp)
    return path

def load_cache(path:str)->list:
    """Load cached content
    
    Parameters
    ----------
    path: str
        File path of cached content

    Returns
    -------
    list: The cached content
    """
    
    with open(path, "r") as fp:
        results = json.load(fp)
    return results

def dump(data:str, path:str):
    """Dump <data> to file located at <path>

    Parameters
    ----------
    data: str
        The data dump
    path: str
        The file path
    """

    with open(path, "w") as fp:
        fp.write(data)
    
def write(lines:[str], path:str):
    """Write <lines> to file located at <path>

    Parameters
    ----------
    lines: [str]
        A list of strings
    path: str
        The file path
    """
    
    with open(path, "w") as fp:   
        fp.write("usrId,env,name,orderId,memos\n") 
        fp.write("\n".join(lines))

def remove(path:str):
    """Remove a file

    Parameters
    ----------
    path: str
        The file path
    """

    try: os.remove(path)
    except FileNotFoundError: pass
