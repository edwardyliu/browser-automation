# project/server/tasks/ina/constant.py

# == Import(s) ==
# => Local
from . import config
from . import utils

# == Constant(s) ==
# => Task
TASK_DICT=utils.get_taskdict(prefix=config.DEFAULT_PREFIX, suffix=config.DEFAULT_SUFFIX)
TASK_KEYS=list(TASK_DICT.keys())
