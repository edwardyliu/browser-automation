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
def main(env:str="linux"):
    print("========================================================")
    print("=== Make Folder(s): ")
    print("========================================================")
    resources = os.path.join(ROOTPATH, "app/resources/")
    logs = os.path.join(ROOTPATH, "app/logs/")
    print(resources)
    if not os.path.exists(resources):
        shell(f"mkdir -p {resources}")
    print(logs)
    if not os.path.exists(logs):
        shell(f"mkdir -p {logs}")

    print("========================================================")
    print("=== Download & Install Geckodriver: ")
    print("========================================================")
    version = "v0.26.0"
    env = env.lower()
    if env == "windows":
        name = "geckodriver-"+version+"-win64.zip"
        command = f"curl -L -O https://github.com/mozilla/geckodriver/releases/download/{version}/{name}"
    elif env == "darwin":
        name = "geckodriver-"+version+"-macos.tar.gz"
        command = f"curl -L -O https://github.com/mozilla/geckodriver/releases/download/{version}/{name}"
    else:
        name = "geckodriver-"+version+"-linux64.tar.gz"
        command = f"curl -L -O https://github.com/mozilla/geckodriver/releases/download/{version}/{name}"
    shell("cd {0} && {1}".format(resources, command))

    stdout = shell(f"cd {resources} && tar -xvzf {name}", show=False)
    shell(f"chmod +x {os.path.join(resources, stdout)}")

if __name__ == "__main__":
    main()
