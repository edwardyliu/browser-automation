# == Import(s) ==
# => System
import os
import re
from pathlib import Path

# == Constant(s) ==
# => General
STARTER_URL="https://www.google.com/"

# => Delay(s)
TASK=1.
JOB=1.

# => Plugin(s)
PLUGINS={
    "ENABLE-PRE-JOB-ADHOC": True, 
    "ENABLE-PRE-BATCH-ADHOC": True, 
    "ENABLE-POST-JOB-ADHOC": True, 
    "ENABLE-POST-BATCH-ADHOC": True, 
    "PRE-JOB-ADHOC": [], 
    "PRE-BATCH-ADHOC": ["make_file"], 
    "POST-JOB-ADHOC": ["submit_job", "scrape_job"], 
    "POST-BATCH-ADHOC": []
}

# => Path & Directories
JSON_DIRPATH=os.path.join(Path(__file__).parents[0], "jsons/")
DRIVER_PATH=os.path.join(Path(__file__).parents[0], "resources/geckodriver")
OUT_DIRPATH=os.path.join(Path(__file__).parents[0], "out/")
OUT_RE=re.compile(r"([0-9]+)\.csv")
