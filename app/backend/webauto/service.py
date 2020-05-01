# == Import(s) ==
# => Local
from . import config
from . import models
from . import utils

# => System
import re
import sys
import time
import uuid

# => Threading
import queue
import threading

# => External
from collections import deque
from selenium import webdriver

# == Service Class(es) ==
class Queue(object):
    """Define a worker queue
    
    """
    
    def __init__(self):
        self.log = utils.get_logger("webauto.queue")
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

    # ==> Getter(s)
    def get_keys(self)->list:
        """Get a list of job key values

        Returns
        -------
        list: The job key values
        """

        return list(self.jobs.keys())

    # ==> Setter(s)
    def reset(self):
        self.stdout = []
    
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
            self.jobs[sequence.key] = sequence

    # ==> Functional
    def enqueue(self, env:str, name:str, fmt:str=None, tbl:dict=None):
        """Enqueue a new job

        Parameters
        ----------
        env: str
            The job environment
        name: str
            The job name
        fmt: str
            The string format
        tbl: dict
            A lookup table
        """

        key = models.Key(name, env)
        self.job_queue.append((key, fmt, tbl))
    
    def dequeue(self):
        """Dequeue (i.e. load & run) the oldest job

        """
        
        key, fmt, tbl = self.job_queue.popleft()
        job = self.jobs.get(key)
        if job:
            if key != self.worker.get_key(): self.worker.load(job)
            else: self.worker.reset()

            results = self.worker.run(tbl)
            if fmt: formatted = utils.parse_job(fmt, tbl, results)
            else: formatted = utils.parse_job(config.DEFAULT_FORMAT, tbl, results)
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
        
        if not filepath: filepath = utils.next_cache_key("save", ".csv")
        with open(filepath, "w") as fp:
            fp.write(",\n".join(self.stdout))
