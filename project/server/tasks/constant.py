# project/server/tasks/constant.py

# == Import(s) ==
from . import utils
from . import config

# == Constant(s) ==
# => Task
TASK_DICT=utils.get_taskdict(prefix=config.DEFAULT_PREFIX, suffix=config.DEFAULT_SUFFIX)
TASK_KEYS=list(TASK_DICT.keys())
