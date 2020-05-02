# == Import(s) ==
# => Local
from . import config

# => System
import re
import logging
import datetime

# => External
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
def parse_expected_condition(driver, raw:str, param:str):
    """Parse the expected condition

    Parameters
    ----------
    driver: webdriver
        The selenium webdriver
    raw: str
        The raw argument; XPATH, Integer, or URL String
    param: str
        The necessary parameter
    """

    if param == "LOCATOR": result = (By.XPATH, raw)
    elif param == "ELEMENT": result = driver.find_element_by_xpath(raw)
    elif param == "INTEGER": result = int(raw)
    else: result = raw
    
    return result

def parse_keyboard(string:str)->str:
    """Parse & funnel any special-key values, replacing them with their corresponding special characters
    
    Parameters
    ----------
    string: str
        The source string
    
    Returns
    -------
    str: The funnelled string
    """

    for replacement in re.findall(config.POSITIONAL, string):
        string = string.replace(replacement, config.KEYS[replacement])
    return string

# => Getter
def next_argv_key(stdout:dict)->str:
    """Get the next available standard-out dictionary key
    
    Parameters
    ----------
    stdout: dict
        The standard-out dictionary
    
    Returns
    -------
    str: An empty key value 
    """
    
    result = "${1}"
    while stdout.get(result):
        pattern = re.findall(config.RE_NUMERAL, result)[0]
        result = result.replace(pattern, str(int(pattern)+1))
    
    return result

def get_webdriver()->webdriver:
    """Get selenium webdriver: geckodriver

    """

    options = webdriver.FirefoxOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(executable_path=config.DEFAULT_WEBDRIVER_EXEPATH, options=options)
    driver.maximize_window()
    return driver

# => Functional
def send_raw_key(ac, logic:str, key:str):
    """Send raw key

    Parameters
    ----------
    ac: ActionChain
        The selenium action chain object
    logic: str
        The keyboard logic
    key: str
        The keyboard character
    """

    if logic == config.KEY_DOWN: ac.key_down(key)
    elif logic == config.KEY_UP: ac.key_up(key)
    else: ac.send_keys(key)

def send_key(ac, elem, logic:str, key:str):
    """Send key

    Parameters
    ----------
    ac: ActionChain
        The selenium action chain object
    elem: WebElement
        The web element
    logic: str
        The keyboard logic
    key: str
        The keyboard character
    """

    if logic == config.KEY_DOWN: ac.key_down(key, element=elem)
    elif logic == config.KEY_UP: ac.key_up(key, element=elem)
    else: ac.send_keys_to_element(elem, key)

def send_keys(driver, elem, argv:list):
    """Send keys

    Parameters
    ----------
    driver: webdriver
        A selenium webdriver
    elem: WebElement
        A web element
    argv: list
        A list of keyboard inputs
    """

    ac = ActionChains(driver)
    for arg in argv:
        if isinstance(arg, list) or isinstance(arg, tuple):
            try:
                logic = arg[0]
                keys = parse_keyboard(arg[1])
            except IndexError: raise IndexError(argv, arg)
        else: 
            logic = "SEND"
            keys = parse_keyboard(arg)

        if logic == "SEND":
            if elem: send_key(ac, elem, logic, keys)
            else: send_raw_key(ac, logic, keys)
        else:
            if elem: 
                for key in keys: send_key(ac, elem, logic, key)
            else: 
                for key in keys: send_raw_key(ac, logic, key)
    ac.perform()
