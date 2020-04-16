# == Import(s) ==
# => Local
from . import constant
from . import model
from . import machine

# => System
import os
import json
from pathlib import Path

# => External
import transitions

def get_dcgs()->list:
    """Get a list of Directed Cycle Graph models via files retrieved from '<basedir>/app/json/.../*.json'

    Returns
    -------
    list:
        A list of Directed Cycle Graph models
    """
    dcgs = []
    for json_file in list( Path(constant.JSON_DIRPATH).rglob("*.[jJ][sS][oO][nN]") ):
        dcg = parse_json(json_file)
        dcgs.append(dcg)
    return dcgs

def parse_json(json_file)->model.DirectedCycleGraph:
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
                arguments:[str] = node[3]
            except IndexError:
                arguments = [str]
            nodes.append( machine.model.Action(name=node[1], key=node[0].lower(), arguments=arguments) )

        return model.DirectedCycleGraph(name=raw["name"], env=raw["environment"], nodes=nodes)
    
    except Exception:
        raise ValueError(f"Parser.parse | Invalid JSON File: {json_file}")
