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
DEFAULT_NA="DELTA"
DEFAULT_URL="https://www.google.com/"
DEFAULT_PREFIX=[]
DEFAULT_SUFFIX=[
    # TODO: Get Order Id & [Optionally] Memos
    ina.Command("GET", DEFAULT_URL, None)
]
