# == Import(s) ==
# => System
import os
import re
from pathlib import Path

# == Configuration(s) & Constant(s) ==
# => Path & Directories
HOMEPAGE_URL="https://www.google.com/"
DEFAULT_SEQUENCE_DIRPATH=os.path.join(Path(__file__).parents[0], "data/")
DEFAULT_CACHE_DIRPATH=os.path.join(Path(__file__).parents[0], "cache/")
DRIVER_EXEPATH=os.path.join(Path(__file__).parents[0], "resources/geckodriver")

# => Regex
RE_NUMERAL_DOT_JSON=re.compile(r"([0-9]+)\.json")
