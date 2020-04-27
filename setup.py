# == Import(s) ==
import os
import subprocess
from pathlib import Path

# == Local Constant(s) ==
ROOTPATH = Path(__file__).parents[0]

# == Utility Function(s) ==
def shell(cmd, show=True):
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
    if show: print(stdout)
    
    try:
        stderr = streams[1].decode("utf-8").strip()
        if stderr: print(stderr)
    except Exception:
        pass
    return stdout

# == Main Function ==
def main(env="linux"):
    print("========================================================")
    print("=== Make Folder(s): ")
    print("========================================================")
    resources = os.path.join(ROOTPATH, "app/backend/webauto/resources/")
    cache = os.path.join(ROOTPATH, "app/backend/webauto/resources/cache/")
    print(resources)
    if not os.path.exists(resources):
        shell("mkdir -p {0}".format(resources), show=False)
    print(cache)
    if not os.path.exists(cache):
        shell("mkdir -p {0}".format(cache), show=False)
    
    print("========================================================")
    print("=== Download & Install Geckodriver: ")
    print("========================================================")
    version = "v0.26.0"
    env = env.lower()
    if env == "windows":
        name = "geckodriver-"+version+"-win64.zip"
        command = "curl -L -O https://github.com/mozilla/geckodriver/releases/download/{0}/{1}".format(version, name)
    elif env == "darwin":
        name = "geckodriver-"+version+"-macos.tar.gz"
        command = "curl -L -O https://github.com/mozilla/geckodriver/releases/download/{0}/{1}".format(version, name)
    else:
        name = "geckodriver-"+version+"-linux64.tar.gz"
        command = "curl -L -O https://github.com/mozilla/geckodriver/releases/download/{0}/{1}".format(version, name)
    shell("cd {0} && {1}".format(resources, command))

    stdout = shell("cd {0} && tar -xvzf {1}".format(resources, name), show=False)
    if not env == "windows": shell("chmod +x {0}".format(os.path.join(resources, stdout)), show=False)

if __name__ == "__main__":
    main()
