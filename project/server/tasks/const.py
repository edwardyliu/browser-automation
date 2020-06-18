# project/server/tasks/const.py

# === Import(s) ===
from . import ina
from . import utils
from . import config

# === Constant(s) ===
TASKS_DICT=utils.get_task_dict(prefix=config.DEFAULT_PREFIX, suffix=config.DEFAULT_SUFFIX)
TASKS_KEYS=list( filter(lambda key: key.env != config.DEFAULT_NA, TASKS_DICT.keys()) )

# => Custom Task(s) <=
TASK_SWAP_USER=TASKS_DICT[ina.Key(config.DEFAULT_NA, "SWAP USER")]
TASK_FIND_ORDER=TASKS_DICT[ina.Key(config.DEFAULT_NA, "FIND ORDER")]
TASK_GET_ORDER_BY_ID=TASKS_DICT[ina.Key(config.DEFAULT_NA, "GET ORDER BY ID")]
TASK_GET_SNAP=TASKS_DICT[ina.Key(config.DEFAULT_NA, "GET SNAP")]