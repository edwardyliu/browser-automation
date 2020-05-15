# project/server/tasks/const.py

# === Import(s) ===
from . import ina
from . import utils
from . import config

# === Constant(s) ===
TASKS_DICT=utils.get_task_dict(prefix=config.DEFAULT_PREFIX, suffix=config.DEFAULT_SUFFIX)
TASKS_KEYS=list( filter(lambda key: key.env != config.DEFAULT_NA, TASKS_DICT.keys()) )

# => Custom Task(s) <=
TASK_FINDBYORDER=TASKS_DICT[ina.Key(config.DEFAULT_NA, "FIND BY ORDER")]
TASK_GETBYID=TASKS_DICT[ina.Key(config.DEFAULT_NA, "GET BY ID")]
TASK_HOTSWAP=TASKS_DICT[ina.Key(config.DEFAULT_NA, "HOT SWAP")]
