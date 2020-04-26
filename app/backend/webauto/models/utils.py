# == Import(s) ==
# => Local
from . import config

# => System
import datetime
import logging
import re

# => External
import pytz
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

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

def parse_expected_condition(driver, raw:str, ec:tuple):
    """Parse the expected condition

    Parameters
    ----------
    driver: webdriver
        The selenium webdriver
    raw: str
        The raw functional argument
    ec: expected condition
        A tuple representing a selenium expected condition
    """

    if ec[1] == "LOCATOR": result = (By.ID, raw)
    elif ec[1] == "ELEMENT": result = driver.find_element_by_xpath(raw)
    elif ec[1] == "INTEGER": result = int(raw)
    else: result = raw
    
    return result

def parse_special_keys(pattern, string:str)->str:
    """Parse special keys, replacing them with their corresponding special character
    
    Parameters
    ----------
    pattern: AnyStr
        The regex compiled pattern
    string: str
        The source string
    
    Returns
    -------
    str: The replaced string
    """

    for replacement in re.findall(pattern, string):
        string = string.replace(replacement, config.SPECIAL_KEYS[replacement])
    return string

def send_raw_key(ac, state:str, key:str):
    """Send raw key

    Parameters
    ----------
    ac: ActionChain
        The selenium action chain object
    state: str
        The key state
    key: str
        The key character
    """

    if state == "KEY_DOWN": ac.key_down(key)
    elif state == "KEY_UP": ac.key_up(key)
    else: ac.send_keys(key)

def send_key(ac, elem, state:str, key:str):
    """Send key

    Parameters
    ----------
    ac: ActionChain
        The selenium action chain object
    elem: WebElement
        The web element
    state: str
        The key state
    key: str
        The key character
    """

    if state == "KEY_DOWN": ac.key_down(key, element=elem)
    elif state == "KEY_UP": ac.key_up(key, element=elem)
    else: ac.send_keys_to_element(elem, key)

def send_keys(driver, elem, items:list):
    """Send keys

    Parameters
    ----------
    driver: webdriver
        The selenium webdriver
    elem: WebElement
        The web element
    items: list
        A list of keyboard-input values
    """

    ac = ActionChains(driver)
    for item in items:
        if isinstance(item, list): 
            state = item[0]
            keys = parse_special_keys(config.POSITIONAL, item[1])
        else: 
            state = "SEND"
            keys = parse_special_keys(config.POSITIONAL, item)

        if state == "SEND":
            if elem: send_key(ac, elem, state, keys)
            else: send_raw_key(ac, state, keys)
        else:
            if elem: 
                for key in keys: send_key(ac, elem, state, key)
            else: 
                for key in keys: send_raw_key(ac, state, key)
    ac.perform()

def next_dict_key(stdout:dict)->str:
    """Get the next available standard-out dictionary key
    
    Parameters
    ----------
    stdout: dict
        The standard-out dictionary
    
    Returns
    -------
    str: An empty key value 
    """
    
    result = "stdout1"
    while stdout.get(result):
        pattern = re.findall(config.RE_NUMERAL, result)[0]
        result = result.replace(pattern, str(int(pattern)+1))
    
    return result
