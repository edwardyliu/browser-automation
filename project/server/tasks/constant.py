# project/server/tasks/constant.py

# == Import(s) ==
from . import ina
from . import utils
from . import config

# == Constant(s) ==
# => Task
TASK_DICT=utils.get_taskdict(prefix=config.PREFIX, suffix=config.SUFFIX)
TASK_KEYS=list(
    filter(
        lambda key: key.env != "ALL", 
        list(TASK_DICT.keys())    
    )
)
TASK_SWITCH=TASK_DICT[ina.Key("ALL", "SWITCH")]
