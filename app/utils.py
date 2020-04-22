# == Import(s) ==
# => Local
from . import constant

# => System
import datetime
import logging
import os
import re

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

def get_available_path()->str:
    path = os.path.join(constant.OUT_DIRPATH, "result1.csv")
    while os.path.isfile(path):
        item = re.findall(constant.OUT_RE, path)[0]
        path = path.replace(item, str(int(item)+1))
    
    return path

def get_driver()->webdriver:
    options = webdriver.FirefoxOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox(executable_path=constant.DRIVER_PATH, options=options)
    return driver
