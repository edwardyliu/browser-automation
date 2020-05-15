# project/server/tasks/config.py

# === Import(s) ===
# => Local <=
from . import ina

# => System <=
import os
import logging
from pathlib import Path

# === Configuration(s) ===
# => Log Level <=
LOG_LEVEL=logging.ERROR

# => Path(s) <=
PATH_JOURNAL=os.path.join(Path(__file__).parents[0], "journal/")

# => Default(s) <=
DEFAULT_NA="STATE CHANGE"
DEFAULT_URL="https://www.google.com/"
DEFAULT_PREFIX=[]
DEFAULT_SUFFIX=[
    ina.Command("GET", DEFAULT_URL, None)
    # TODO: Get Order Id & [Optionally] Memos
]
