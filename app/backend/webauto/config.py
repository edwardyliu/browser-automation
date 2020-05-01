# == Import(s) ==
# => Local
from . import models

# => System
import os
import re
from pathlib import Path

# == Configuration(s) & Constant(s) ==
# => Path & Directories
DEFAULT_HOMEPAGE_URL="https://www.google.com/"
DEFAULT_SEQUENCE_DIRPATH=os.path.join(Path(__file__).parents[0], "data/")
DEFAULT_CACHE_DIRPATH=os.path.join(Path(__file__).parents[0], "resources/cache/")
DEFAULT_DRIVER_EXEPATH=os.path.join(Path(__file__).parents[0], "resources/geckodriver")

# => Format
DEFAULT_FORMAT="argv: ${@}, tblv: ${@#}"

# => Regex
RE_NUMERAL_DOT_JSON=re.compile(r"([0-9]+)\.json")
POSITIONAL=re.compile(r"(\$\{.*?\})")
ARGV="@"
TBLV="@#"

# => Middleware(s)
DEFAULT_PREFIX_MIDDLEWARE=[
    models.Command("GET", DEFAULT_HOMEPAGE_URL, None)
]
DEFAULT_POSTFIX_MIDDLEWARE=[
    models.Command("GET", DEFAULT_HOMEPAGE_URL, None),
    models.Command(
        "PRINTF", 
        "web_element: ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}, inner_argv: ${@}", 
        ["A", "Beautiful", "Mind"])
]
