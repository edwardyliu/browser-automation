# == Import(s) ==
import os
from pathlib import Path

# == Constant(s) ==
# => Controller
ALTER=1.
JOB=1.

# => Parser
JSON_DIRPATH=os.path.join(Path(__file__).parents[0], "jsons/")

# => Utils
DRIVER_PATH=os.path.join(Path(__file__).parents[0], "resources/geckodriver")
