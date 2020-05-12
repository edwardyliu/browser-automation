# project/server/tasks/const.py

# == Import(s) ==
from . import ina
from . import utils
from . import config

# == Constant(s) ==
# => Task Collection(s)
TASKDICT=utils.get_taskdict(prefix=config.PREFIX, suffix=config.SUFFIX)
TASKKEYS=list( filter(lambda key: key.env != config.NOT_APPLICABLE, TASKDICT.keys()) )

# => Task(s)
TASK_FINDBYORDER=TASKDICT[ina.Key(config.NOT_APPLICABLE, "FIND BY ORDER")]
TASK_GETBYID=TASKDICT[ina.Key(config.NOT_APPLICABLE, "GET BY ID")]
TASK_HOTSWAP=TASKDICT[ina.Key(config.NOT_APPLICABLE, "HOT SWAP")]
