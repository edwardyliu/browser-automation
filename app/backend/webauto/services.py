# == Import(s) ==
# => Local
from . import config
from . import models
from . import utils

# => System
import re
import time
import uuid
from collections import deque

# => External
from selenium import webdriver

class Controller(object):
    """Define a Controller
    
    """

    def __init__(self):
        self.log = utils.get_logger("webauto.controller")
        self.worker = models.Worker(str(uuid.uuid4()), utils.get_webdriver())
        
        self.job_queue = deque([])
        self.stdout = []
        self.set_middleware(config.DEFAULT_PREFIX_MIDDLEWARE, config.DEFAULT_POSTFIX_MIDDLEWARE)

    def __del__(self):
        if self.stdout: utils.cache(self.stdout)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def get_job_keys(self)->list:
        """Get a list of job key values

        Returns
        -------
        list: The job key values
        """

        return list(self.jobs.keys())

    def set_middleware(self, prefix:list, postfix:list):
        """Set universal middlewares

        Parameters
        ----------
        prefix: list
            A list of command objects
        postfix: list
            A list of command objects
        """

        self.prefix = prefix
        self.postfix = postfix
        self.jobs = {}
        for sequence in utils.get_sequences(): 
            sequence.extendleft(self.prefix)
            sequence.extend(self.postfix)
            self.jobs[sequence.name] = sequence

    def enqueue(self, key:str, fmt:str=None, argv:dict=None):
        """Enqueue a new job

        Parameters
        ----------
        key: str
            The job key
        fmt: str
            The string format
        argv: dict
            A lookup table
        """

        self.job_queue.append((key, fmt, argv))
    
    def dequeue(self):
        """Dequeue (i.e. load & run) the oldest job

        """

        key, fmt, argv = self.job_queue.popleft()
        job = self.jobs.get(key)
        if job:
            self.worker.load(job)
            results = self.worker.run()
            if fmt: formatted = utils.parse_job(fmt, argv, results)
            else: formatted = utils.parse_job(config.DEFAULT_FORMAT, argv, results)
            self.stdout.append(formatted)

    def submit(self):
        """Dequeue until the job queue is empty

        """

        while len(self.job_queue) > 0: self.dequeue()

    def save(self, filepath:str=None):
        """Save as CSV file

        Parameters
        ----------
        filepath: str
            Where to save the file
        """
        
        if not filepath: filepath = utils.next_key("save", ".csv")
        with open(filepath, "w") as fp:
            fp.write(",\n".join(self.stdout))
        self.stdout = []
    