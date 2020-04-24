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

def get_next_outpath()->str:
    """Get the next available <outpath>.csv

    """
    path = os.path.join(config.OUT_DIRPATH, "result1.csv")
    while os.path.isfile(path):
        item = re.findall(config.OUT_RE, path)[0]
        path = path.replace(item, str(int(item)+1))
    
    return path

def get_driver()->webdriver:
    """Get the geckodriver selenium webdriver

    """
    options = webdriver.FirefoxOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox(executable_path=config.DRIVER_PATH, options=options)
    return driver

def get_filepaths()->list:
    """Get a list of file paths retrieved from '<basedir>/app/json/.../*.json'

    Returns
    -------
    list:
        A list of file paths
    """
    return list( Path(config.JSON_DIRPATH).rglob("*.[jJ][sS][oO][nN]") )

def get_dcgs()->list:
    """Get a list of Directed Cycle Graph models via files retrieved from '<basedir>/app/json/.../*.json'

    Returns
    -------
    list:
        A list of Directed Cycle Graph models
    """
    dcgs = []
    for json_file in list( Path(config.JSON_DIRPATH).rglob("*.[jJ][sS][oO][nN]") ):
        dcg = parse_json(json_file)
        dcgs.append(dcg)
    return dcgs

def parse_json(json_file)->models.DirectedCycleGraph:
    """Parse a JSON file into a Directed Cycle Graph model

    Parameters
    ----------
    json_file: str
        The JSON file path

    Returns
    -------
    model.DirectedCycleGraph:
        The model object
    """
    try:
        with open(json_file) as fptr:
            raw = json.load(fptr)

        nodes = []
        for node in raw["graph"]:
            try:
                arguments = node[3]
                if not isinstance(arguments, list):
                    arguments = [arguments]
            except IndexError:
                arguments = [str]
            nodes.append( models.Action(name=node[1], key=node[0].lower(), arguments=arguments) )

        return models.DirectedCycleGraph(name=raw["name"], env=raw["environment"], nodes=nodes)
    
    except Exception:
        raise ValueError(f"Parser.parse | Invalid JSON File: {json_file}")
