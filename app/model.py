# == Import(s) ==
# => System
from dataclasses import dataclass

# == Data Model(s) ==
@dataclass(frozen=True)
class DirectedCycleGraph:
    """Define a Directed Cycle Graph

    A finite state machine cycle is constructed with <nodes>: 
        i.e. 1=>2=>...=>N=>1
    """
    name: str
    env: str
    nodes: list
