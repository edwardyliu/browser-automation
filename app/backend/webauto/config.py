# == Import(s) ==
# => Local
from . import models

# => System
import os
import re
from pathlib import Path

# == Configuration(s) ==
# => Path & Directories
DEFAULT_TASK_DIRPATH=os.path.join(Path(__file__).parents[0], "tasks/")
DEFAULT_CACHE_DIRPATH=os.path.join(Path(__file__).parents[0], "resources/cache/")

# => Regex(s)
RE_NUMERAL=re.compile(r"([0-9]+)")
POSITIONAL=re.compile(r"(\$\{.*?\})")

# => Constant(s)
DEFAULT_STRING_FORMAT="argv: ${@}, tblv: ${@#}"
ARGV="@"
TBLV="@#"

# => Middleware(s)
DEFAULT_HOMEPAGE_URL="https://www.google.com/"
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
