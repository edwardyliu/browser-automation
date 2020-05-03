# project/server/tasks/ina/utils.py

# == Import(s) ==
# => Local
from . import config
from . import models

# => System
import os
import re
import json
import logging
import datetime
from pathlib import Path
from collections import deque

# => External
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    log.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fmt.converter = timezone_converter_est

    handle = logging.StreamHandler()
    handle.setLevel(logging.INFO)
    handle.setFormatter(fmt)
    log.addHandler(handle)
    return log

def next_argv_key(results:dict)->str:
    """Get the next available key in the 'results' dictionary
    
    Parameters
    ----------
    results: dict
        A dictionary
    
    Returns
    -------
    str: The next available key value 
    """
    
    key = "${1}"
    while results.get(key):
        pattern = re.findall(config.RE_NUMERAL, key)[0]
        key = key.replace(pattern, str(int(pattern)+1))
    return key

def next_cache_key(prefix:str, postfix:str)->str:
    """Get the next available '<prefix>r"([0-9]+)"<postfix>' filepath

    Parameters
    ----------
    prefix: str
        The prefix string
    postfix: str
        The postfix string

    Returns
    -------
    str: The next available filepath 
    """

    filepath = os.path.join(config.CACHE_DIRPATH, f"{prefix}1{postfix}")
    while os.path.isfile(filepath):
        pattern = re.findall(config.RE_NUMERAL, filepath)[0]
        filepath = filepath.replace(pattern, str(int(pattern)+1))
    return filepath

def get_webdriver()->webdriver:
    """Get Selenium WebDriver: geckodriver

    """

    options = webdriver.FirefoxOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox(executable_path=config.WEBDRIVER_EXEPATH, options=options)
    driver.maximize_window()
    return driver

def get_tasklist(log:logging.Logger=None, prefix:list=None, suffix:list=None)->list:
    """Get a list of task objects from "<basedir>/tasks/.../*.json"

    Returns
    -------
    list: A list of task objects
    """

    tasks = []
    for filepath in list(Path(config.TASK_DIRPATH).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"parsing task: {filepath}")
        task = parse_json(filepath)
        if prefix: task.extendleft(prefix)
        if suffix: task.extend(suffix)
        tasks.append(task)

    return tasks

def get_taskdict(log:logging.Logger=None, prefix:list=None, suffix:list=None)->dict:
    """Get a list of task objects from "<basedir>/tasks/.../*.json"

    Returns
    -------
    dict: A dictionary of task objects
    """
    
    tasks = {}
    for filepath in list(Path(config.TASK_DIRPATH).rglob("*.[jJ][sS][oO][nN]")):
        if log: log.info(f"parsing task: {filepath}")
        task = parse_json(filepath)
        if prefix: task.extendleft(prefix)
        if suffix: task.extend(suffix)
        tasks[task.key] = task

    return tasks

# => Parser(s)
def parse_json(filepath:str)->models.Task:
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
            
            cmds.append(models.Command(label, target, argv))
        return models.Task(models.Key(raw["env"], raw["name"]), cmds)
    
    except IndexError: raise IndexError(f"ina.models.utils.parse_json: Index Error - {filepath}")

def parse_task_response(fmt:str, lut:dict, response:dict)->str:
    """Parse task response into a formatted string

    Parameters
    ----------
    fmt: str
        The string format
    lut: dict
        A lookup table
    response: dict
        The resulting lookup table generated by the task
    
    Returns
    -------
    str: The formatted string
    """

    for elem in re.findall(config.POSITIONAL, fmt):
        value = elem[2:-1]
        if value == config.LUTV: fmt = fmt.replace(elem, json.dumps(lut))
        elif value == config.ARGV:
            span = []; result = response.get("${1}")
            while result:
                span.append(result)
                result = response.get("${" + str(len(span)+1) + "}")
            fmt = fmt.replace(elem, ", ".join(span))
        elif value.isdigit(): fmt = fmt.replace(elem, response.get(elem, "N/A"))
        else: fmt = fmt.replace(elem, lut.get(value, "None"))
    
    return fmt

def parse_expected_condition(driver, target:str, param:str):
    """Parse expected condition

    Parameters
    ----------
    driver: WebDriver
        The Selenium WebDriver
    target: str
        The argument - an XPATH value, Integer value, or URL string
    param: str
        The parameter - a LOCATOR, ELEMENT, or INTEGER
    """

    if param == "LOCATOR": result = (By.XPATH, target)
    elif param == "ELEMENT": result = driver.find_element_by_xpath(target)
    elif param == "INTEGER": result = int(target)
    else: result = target
    
    return result

def parse_keyboard(string:str)->str:
    """Parse & funnel special keyboard values, replace w/ corresponding special characters.
    
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

# => Functional
def send_key_raw(ac, logic:str, key:str):
    """Send raw key

    Parameters
    ----------
    ac: ActionChain
        The Selenium ActionChain object
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
        The Selenium ActionChain object
    elem: WebElement
        A Selenium WebElement
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
    driver: WebDriver
        The Selenium WebDriver
    elem: WebElement
        The web element
    argv: list
        A list of keyboard inputs
    """

    ac = ActionChains(driver)
    for arg in argv:
        if isinstance(arg, list) or isinstance(arg, tuple):
            try:
                logic = arg[0]
                keys = parse_keyboard(arg[1])
            except IndexError: raise IndexError(f"ina.models.utils.send_keys: IndexError '{argv}' - {arg}")
        else: 
            logic = "SEND"
            keys = parse_keyboard(arg)

        if logic == "SEND":
            if elem: send_key(ac, elem, logic, keys)
            else: send_key_raw(ac, logic, keys)
        else:
            if elem: 
                for key in keys: send_key(ac, elem, logic, key)
            else: 
                for key in keys: send_key_raw(ac, logic, key)
    ac.perform()

def cache(results:list)->str:
    """Cache <results>
    
    Parameters
    ----------
    results: list
        A list of printf strings

    Returns
    -------
    str: The cached filepath
    """

    filepath = next_cache_key("cache", ".json")
    with open(filepath, "w") as fp:
        json.dump(results, fp)
    return filepath

def load_cache(filepath:str)->list:
    """Load the cached results
    
    Parameters
    ----------
    filepath: str
        The filepath of the cached content

    Returns
    -------
    list: The cached content
    """
    
    with open(filepath, "r") as fp:
        results = json.load(fp)
    return results

# => Functional: E-mail
# TODO: create E-mail template & implement E-mail functionality
