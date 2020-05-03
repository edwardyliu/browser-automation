# project/server/tasks/ina/job.py

# == Import(s) ==
# => Local
from . import utils
from . import config
from . import models
from . import driver
from . import constant

# => System
import uuid
from collections import deque

# == Object Definition ==
class Job(object):
    """ Define a job

    A list of tasks
    """

    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.log = utils.get_logger(f"ina.job.{self.uid}")

        self.driver = None
        self.queue = deque([])
        self.results = []

    def __del__(self):
        if self.driver: del self.driver
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
    
    # ==> Setter(s)
    def reset(self):
        """Reset task list

        """

        self.queue.clear()
        self.results.clear()
        
    # ==> Functional
    def exec(self, requestor:str=None):
        """Pop task list until queue is empty; respond back to requestor

        """

        if not self.driver: self.driver = driver.Driver(self.uid)
        while len(self.queue) > 0: self.pop()
        self.respond(requestor)
    
    def push(self, key:models.Key, fmt:str=None, lut:dict=None):
        """Push (i.e. enqueue) a new task

        Parameters
        ----------
        key: models.Key
            The task key
        fmt: str, optional
            The string format
        lut: dict, optional
            A lookup table
        """

        self.queue.append((key, fmt, lut))

    def push_(self, env:str, name:str, fmt:str=None, lut:dict=None):
        """Push (i.e. enqueue) a new task

        Parameters
        ----------
        env: str
            The task environment
        name: str
            The task name
        fmt: str, optional
            The string format
        lut: dict, optional
            A lookup table
        """

        key = models.Key(env, name)
        self.queue.append((key, fmt, lut))
    
    def pop(self):
        """Pop (i.e. dequeue - assign & work) the oldest task

        """
        
        key, fmt, lut = self.queue.popleft()
        task = constant.TASK_DICT.get(key)
        if task:
            if key != self.driver.key(): self.driver.assign(task)
            else: self.driver.reset()

            response = self.driver.run(lut)
            if fmt: formatted = utils.parse_task_response(fmt, lut, response)
            else: formatted = utils.parse_task_response(config.DEFAULT_STRING_FORMAT, lut, response)
            
            self.results.append(formatted)
    
    def respond(self, requestor:str):
        """Save as CSV file

        Parameters
        ----------
        requestor: str
            The requestor's E-mail
        """
        
        filepath = utils.next_cache_key("save", ".csv")
        with open(filepath, "w") as fp:
            fp.write(",\n".join(self.results))

        # TODO: E-mail the result list to the requestor
