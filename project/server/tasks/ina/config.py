# project/server/tasks/ina/config.py

# === Import(s) ===
# => Local <=
from . import const

# => System <=
import os
import logging
from pathlib import Path

# === Configuration(s) ===
# => Log Level <=
LOG_LEVEL=logging.ERROR

# => Path(s) <=
PATH_CACHE=os.path.join(Path(__file__).parents[0], "resources/cache/")
PATH_WEBDRIVER=os.path.join(Path(__file__).parents[0], "resources/geckodriver")

# => Default(s) <=
DEFAULT_WAIT=0.5
DEFAULT_TIMEOUT=5.0
DEFAULT_FORMAT=(
    "${usrId}," +       # user ID
    "${0}," +           # env, name
    "${" + const.LAST + "}"   # order ID, [Optionally] memos
)

DEFAULT_SMTP_SERVER="127.0.0.1"
DEFAULT_SMTP_PORT=25
DEFAULT_SENDER_EMAIL="support@nauto.com"