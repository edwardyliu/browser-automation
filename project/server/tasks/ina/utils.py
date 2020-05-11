# project/server/tasks/ina/utils.py

# == Import(s) ==
# => Local
from . import config

# => System
import os
import re
import json
import logging
import datetime

# => External
import pytz
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

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

def cachekey(prefix:str, postfix:str)->str:
    """Get next available file path of the format:
    <prefix>r"([0-9]+)"<postfix> starting from '1'

    Parameters
    ----------
    prefix: str
        The prefix string
    postfix: str
        The postfix string

    Returns
    -------
    str: The next available file path 
    """

    filepath = os.path.join(config.CACHE_DIRPATH, f"{prefix}1{postfix}")
    while os.path.isfile(filepath):
        pattern = re.findall(config.RE_NUMERAL, filepath)[0]
        filepath = filepath.replace(pattern, str(int(pattern)+1))
    return filepath

# => Functional
def cache(results:list)->str:
    """Cache <results>
    
    Parameters
    ----------
    results: list
        A list of printf strings

    Returns
    -------
    str: The cached file path
    """

    filepath = cachekey("cache", ".json")
    with open(filepath, "w") as fp:
        json.dump(results, fp)
    return filepath

def cacheload(filepath:str)->list:
    """Load the cached results
    
    Parameters
    ----------
    filepath: str
        The file path of the cached content

    Returns
    -------
    list: The cached content
    """
    
    with open(filepath, "r") as fp:
        results = json.load(fp)
    return results

def write(lines:[str], filepath:str):
    """Write lines to file

    Parameters
    ----------
    lines: [str]
        A list of strings
    filepath: str
        The file path
    """
    lines.insert(0, "usrId,env,name,orderId,memos")

    with open(filepath, "w") as fp:    
        fp.write("\n".join(lines))

def remove(filepath:str):
    """Remove file

    Parameters
    ----------
    filepath: str
        The file path
    """

    try: os.remove(filepath)
    except FileNotFoundError: pass
