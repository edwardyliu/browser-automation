# == Import(s) ==
# => System
from dataclasses import dataclass

# => External
import transitions

# == Data Model(s) ==
@dataclass(frozen=True)
class Method:
    """Define a method/function execution strategy:

    Execute a method/function given a keyword <action> and a list of string parameters <arguments>
    """
    action: str
    arguments: [str]

@dataclass(frozen=True)
class DirectedCycleGraph:
    """Define a Directed Cycle Graph

    A finite state machine can be constructed using:
        1. nodes: the states
        2. connections: the transitions
        3. methods: the actions
    """
    name: str
    environment: str

    nodes: [transitions.State]
    connections: [dict]
    methods: [Method]
