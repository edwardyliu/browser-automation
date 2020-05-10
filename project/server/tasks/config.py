# project/server/tasks/config.py

# == Import(s) ==
# => Local
from . import ina

# => System
import os
import logging
from pathlib import Path

# == Configuration(s) ==
# => Logging
LOG_LEVEL=logging.ERROR

# => Path & Directories
JOURNAL_DIRPATH=os.path.join(Path(__file__).parents[0], "journal/")

# => Default(s)
DEFAULT_URL="https://www.google.com/"
PREFIX=[]
SUFFIX=[
    ina.Command("GET", DEFAULT_URL, None)
    # TODO: Get Order Id & [Optionally] Memos
]
