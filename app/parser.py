# == Import(s) ==
# => Local
from . import constant
from . import model

# => System
import os
import json
from pathlib import Path

# => External
import transitions

def get()->[model.DirectedCycleGraph]:
    dcgs = [model.DirectedCycleGraph]
    for json_file in list( Path(constant.JSON_DIRPATH).rglob("*.[jJ][sS][oO][nN]") ):
        dcgs.append( parse(json_file) )
    return dcgs

def parse(json_file)->model.DirectedCycleGraph:
    
    try:
        with open(json_file) as fptr:
            raw = json.load(fptr)

        nodes = [transitions.State]
        connections = [dict]
        methods = [model.Method]
        for node in raw["graph"]:
            nodes.append(transitions.State(name=node[1]))
            connections.append({
                "trigger": node[0].lower(), 
                "source": node[1], 
                "dest": node[2]
            })
            try:
                arguments = node[3]
            except IndexError:
                arguments = [str]
            methods.append( model.Method(node[0], arguments) )

        return model.DirectedCycleGraph(raw["name"], raw["environment"], nodes, connections, methods)
    
    except Exception:
        raise ValueError(f"Parser.parse | Invalid JSON File: {json_file}")

if __name__ == "__main__":
    dcgs = get()
    print( dcgs )