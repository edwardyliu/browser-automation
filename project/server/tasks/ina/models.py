# project/server/tasks/ina/models.py

# == Import(s) ==
# => System
from collections import deque
from dataclasses import dataclass

# == Data Model(s) ==
@dataclass(frozen=True)
class Command:
    """Define a Command: Execute a command

    Parameters
    ----------
    label: str
        Command label
    target: str
        Primary command argument
    argv: list
        Secondary command arguments
    """

    label: str
    target: str
    argv: list

    def __str__(self):
        return f"INA.Command(label={self.label})"

@dataclass(frozen=True)
class Key:
    """Define a Key: The ID of a sequence object

    Parameters
    ----------
    env: str
        The task environment
    name: str
        The task name
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
    """Define a Task: A sequence is a list of Command(s) to be executed linearly

    Parameters
    ----------
    key: models.Key
        The ID
    cmds: deque of models.Command(s)
        A queue of commands
    """

    key: Key
    cmds: deque

    def __str__(self):
        return f"INA.Task(key={self.key})"

    def push(self, cmd:Command):
        """Push a new command to the rightmost position

        Parameters
        ----------
        cmd: Command
            A command object
        """

        self.cmds.append(cmd)

    def pushleft(self, cmd:Command):
        """Push a new command to the leftmost position
        
        Parameters
        ----------
        cmd: Command
            A command object
        """

        self.cmds.appendleft(cmd)

    def extend(self, cmds:list):
        """Extend a list of new commands, in order, to the rightmost position
        
        Parameters
        ----------
        cmds: list
            A list of command objects
        """

        self.cmds.extend(cmds)

    def extendleft(self, cmds:list):
        """Extend a list of new commands, in order, to the leftmost position
        
        Parameters
        ----------
        cmds: list
            A list of command objects
        """

        for cmd in reversed(cmds): self.cmds.appendleft(cmd)

    def pop(self)->Command:
        """Pop the rightmost command away from the command list
        
        Returns
        -------
        Command: The popped command object
        """

        return self.cmds.pop()

    def popleft(self)->Command:
        """Pop the leftmost command away from the command list
        
        Returns
        -------
        Command: The popped command object
        """

        return self.cmds.popleft()
