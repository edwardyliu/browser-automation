# == Import(s) ==
import os
import re
from pathlib import Path

# == Constant(s) ==
# => Controller
INITIAL_PAGE="https://www.google.com/"
TASK=1.
JOB=1.

OUT_DIRPATH=os.path.join(Path(__file__).parents[0], "out/")
OUT_RE=re.compile(r"([0-9]+)\.csv")

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

# => Parser
JSON_DIRPATH=os.path.join(Path(__file__).parents[0], "jsons/")

# => Utils
DRIVER_PATH=os.path.join(Path(__file__).parents[0], "resources/geckodriver")
