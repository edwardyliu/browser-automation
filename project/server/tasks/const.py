# project/server/tasks/const.py

# == Import(s) ==
from . import ina
from . import utils
from . import config

# == Constant(s) ==
# => Task
TASKDICT=utils.get_taskdict(prefix=config.PREFIX, suffix=config.SUFFIX)
TASKKEYS=list(
    filter(
        lambda key: key.env != config.NOT_APPLICABLE, 
        list(TASKDICT.keys())    
    )
)

# => Task Key
TASK_HOTSWAP=TASKDICT[ina.Key(config.NOT_APPLICABLE, "HOTSWAP")]
TASK_SEARCH=TASKDICT[ina.Key(config.NOT_APPLICABLE, "SEARCH")]
TASK_FIND=TASKDICT[ina.Key(config.NOT_APPLICABLE, "FIND")]
