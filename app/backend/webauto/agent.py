# == Import(s) ==
# => Local
from . import config
from . import utils
from . import models

# => System
import uuid

# => External
from collections import deque

# == Object Class ==
class Agent(object):
    """Define an agent
    
    """
    
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.log = utils.get_logger(f"WebAuto.agent.{self.uid}")

        self.worker = None
        self.queue = deque([])
        self.results = []
        self.set_middleware(config.DEFAULT_PREFIX_MIDDLEWARE, config.DEFAULT_POSTFIX_MIDDLEWARE)

    def __del__(self):
        if self.worker: del self.worker
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    # ==> Getter(s)
    def get_keys(self)->list:
        """Get a list of task key values

        Returns
        -------
        list: The list of task key values
        """

        return list(self.tasks.keys())

    # ==> Setter(s)
    def reset(self):
        """Reset the task list

        """

        self.worker = None
        self.queue.clear()
        self.results = []
        
    def set_middleware(self, prefix:list, postfix:list):
        """Set universal middlewares

        Parameters
        ----------
        prefix: list
            A list of command objects
        postfix: list
            A list of command objects
        """

        self.tasks = {}
        for task in utils.get_tasks(): 
            task.extendleft(prefix)
            task.extend(postfix)
            self.tasks[task.key] = task

    # ==> Functional
    def exec(self, requestor:str=None):
        """Pop until the work queue is empty

        """

        if not self.worker: self.worker = models.Worker(self.uid)
        while len(self.queue) > 0: self.pop()
        self.respond(requestor)
    
    def push(self, env:str, name:str, fmt:str=None, tbl:dict=None):
        """Push (i.e. enqueue) a new task

        Parameters
        ----------
        env: str
            The task environment
        name: str
            The task name
        fmt: str
            The string format
        tbl: dict
            A lookup table
        """

        key = models.Key(name, env)
        self.queue.append((key, fmt, tbl))
    
    def pop(self):
        """Pop (i.e. dequeue - assign & run) the oldest task

        """
        
        key, fmt, tbl = self.queue.popleft()
        task = self.tasks.get(key)
        if task:
            if key != self.worker.key(): self.worker.assign(task)
            else: self.worker.reset()

            response = self.worker.run(tbl)
            if fmt: formatted = utils.parse_task(fmt, tbl, response)
            else: formatted = utils.parse_task(config.DEFAULT_STRING_FORMAT, tbl, response)
            self.results.append(formatted)
    
    def respond(self, requestor:str):
        """Save as CSV file

        Parameters
        ----------
        filepath: str
            Where to save the file
        """
        
        if not filepath: filepath = utils.next_cache_key("save", ".csv")
        with open(filepath, "w") as fp:
            fp.write(",\n".join(self.results))

        # TODO: E-mail the result list to the requestor