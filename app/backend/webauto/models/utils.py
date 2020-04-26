# == Import(s) ==
# => Local
from . import config

# => System
import datetime
import logging
import re

# => External
import pytz
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

def get_parsed_expected_condition(driver, raw:str, ec:tuple):
    """Get parsed expected condition

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

def get_next_stdout(stdout:dict)->str:
    """Get the next available standard-out key

    Parameters
    ----------
    stdout: dict
        The standard-out dictionary
    """

    result = "stdout1"
    while stdout.get(result):
        pattern = re.findall(config.RE_NUMERAL, result)[0]
        result = result.replace(pattern, str(int(pattern)+1))
    
    return result
