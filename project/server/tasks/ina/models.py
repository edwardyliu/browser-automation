# project/server/tasks/ina/models.py

# === Import(s) ===
# => System <=
from collections import deque
from dataclasses import dataclass

# === Data Model(s) ===
@dataclass(frozen=True)
class Command:
    """Define a Command Object
    
    For executing a particular command

    Parameters
    ----------
    label: str
        A command label
    target: str
        The primary command argument
    argv: list
        A list of secondary command arguments
    """

    label: str
    target: str
    argv: list

    def __str__(self):
        return f"INA.Command(label={self.label})"

@dataclass(frozen=True)
class Key:
    """Define a Key Object
    
    Is the unique ID of a Task object

    Parameters
    ----------
    env: str
        The Task environment
    name: str
        The Task name
    """

    env: str
    name: str

    def __hash__(self):
        return hash(self.env + self.name)

    def __eq__(self, another):
        return (
            hasattr(another, "env") and self.env == another.env and 
            hasattr(another, "name") and self.name == another.name)

    def __str__(self):
        return f"INA.Key(env={self.env}, name={self.name})"

@dataclass(frozen=True)
class Task:
    """Define a Task Object
    
    Is a sequence of Command objects executed linearly

    Parameters
    ----------
    key: Key
        The Task ID
    cmds: deque
        A deque list of Command objects
    """

    key: Key
    cmds: deque

    def __str__(self):
        return f"INA.Task(key={self.key})"

    def push(self, cmd:Command):
        """Push new command to rightmost position

        Parameters
        ----------
        cmd: Command
            A command object
        """

        self.cmds.append(cmd)

    def pushleft(self, cmd:Command):
        """Push new command to leftmost position
        
        Parameters
        ----------
        cmd: Command
            A command object
        """

        self.cmds.appendleft(cmd)

    def extend(self, cmds:list):
        """Extend a list of new commands to rightmost position
        
        Parameters
        ----------
        cmds: list
            A list of command objects
        """

        self.cmds.extend(cmds)

    def extendleft(self, cmds:list):
        """Extend a list of new commands, in-order, to leftmost position
        
        Parameters
        ----------
        cmds: list
            A list of command objects
        """

        for cmd in reversed(cmds): self.cmds.appendleft(cmd)

    def pop(self)->Command:
        """Pop rightmost command from command list
        
        Returns
        -------
        Command: The popped command object
        """

        return self.cmds.pop()

    def popleft(self)->Command:
        """Pop leftmost command from command list
        
        Returns
        -------
        Command: The popped command object
        """

        return self.cmds.popleft()
