# == Import(s) ==
# => System
import datetime
import logging

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

def parse_expected_condition(driver, raw:str, ec:tuple):
    if ec[1] == "LOCATOR":
        res = (By.ID, raw)
    elif ec[1] == "ELEMENT":
        res = driver.find_element_by_xpath(raw) 
    elif ec[1] == "INTEGER":
        res = int(raw)
    else: # String
        res = raw
    
    return res
