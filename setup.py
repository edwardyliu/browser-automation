# == Import(s) ==
import os
import subprocess
from pathlib import Path

# == Local Constant(s) ==
ROOTPATH = Path(__file__).parents[0]

# == Utility Function(s) ==
def shell(cmd:str, show:bool=True)->str:
    """Execute shell <cmd>

    Parameters
    ----------
    cmd: str
        The shell command to execute
    show: bool, optional
        Whether or not to stream the command output to standard out
        By default: True

    Returns
    -------
    str:
        The command output generated from the shell command
    """
    streams = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
    stdout = streams[0].decode("utf-8").strip()
    stderr = streams[1].decode("utf-8").strip()
    if stderr: print(stderr)
    if show: print(stdout)
    return stdout

# == Main Function ==
def main():
    print("main")

if __name__ == "__main__":
    main()
