# project/server/tasks/ina/job.py

# == Import(s) ==
# => Local
from . import utils
from . import config
from . import models
from . import driver
from . import template

# => System
import uuid
import smtplib
import datetime
from collections import deque
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# == Object Definition ==
class Job(object):
    """ Define a job

    A list of tasks
    """

    def __init__(self, uid:str=None):
        self.id = uid or str(uuid.uuid4())
        self.log = utils.get_logger(f"ina.job.{self.id}")
        self.dt = datetime.datetime.now()

        self.driver = None
        self.queue = deque([])
        self.lines = []

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
        self.lines.clear()
        
    # ==> Functional
    def exec(self, receiver:str=None):
        """Pop task list until queue is empty; respond back to receiver

        """

        if len(self.queue) > 0:
            if not self.driver: self.driver = driver.Driver(self.id)
            while len(self.queue) > 0: self.pop()
            if receiver: self.notify(receiver)
        
    def push(self, task:models.Task, fmt:str=None, lut:dict=None):
        """Push (i.e. enqueue) a new task

        Parameters
        ----------
        task: models.Task
            The task
        fmt: str, optional
            The string format
        lut: dict, optional
            A lookup table
        """

        self.queue.append((task, fmt, lut))
    
    def pop(self):
        """Pop (i.e. dequeue - assign & work) the oldest task

        """
        
        task, fmt, lut = self.queue.popleft()
        if task:
            if task.key != self.driver.key(): self.driver.assign(task)
            else: self.driver.reset()

            response = self.driver.run(lut)
            if fmt: line = utils.parse_task_response(fmt, lut, response)
            else: line = utils.parse_task_response(config.DEFAULT_STRING_FORMAT, lut, response)
            self.lines.append(line)
    
    def notify(self, receiver:str):
        """Notify the receiver of job

        Parameters
        ----------
        receiver: str
            An E-mail address
        """
        
        filepath = utils.get_absolute_path(f"{self.id}.csv")
        utils.write(self.lines, filepath)
        attachment = utils.get_email_attachment(filepath)
        self.send_mail(receiver, attachment=attachment)
        utils.remove(filepath)

    def send_mail(self, receiver:str, attachment=None):
        """Send mail
        
        Parameters
        ----------
        receiver: str
            The receiver's e-mail address
        content: list
            A list of strings
        """

        sender = config.DEFAULT_SENDER_EMAIL

        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = "Nauto Report"

        # == HTML E-mail ==
        body = template.body_meta(taskid=self.id, dt=self.dt)
        body += template.body_information(email=sender)
        body += template.body_content_head("User ID", "Env", "Name", "Order ID")
        if len(self.lines) > 0:
            lastrow = self.lines[-1].split(",")
            for line in self.lines[:-1]:
                row = line.split(",")
                body += template.body_content_item(
                    utils.iget(row, 0), utils.iget(row, 1), utils.iget(row, 2), utils.iget(row, 3), False)
            body += template.body_content_item(
                utils.iget(lastrow, 0), utils.iget(lastrow, 1), utils.iget(lastrow, 2), utils.iget(lastrow, 3), True)
        body += template.body_content_summary(True)
        html = template.header + body + template.footer(email=sender)

        message.attach(MIMEText(template.text(True), "plain"))
        message.attach(MIMEText(html, "html"))

        # == Add Attachment ==
        if attachment: message.attach(attachment)

        # == Send The E-mail ==
        text = message.as_string()
        with smtplib.SMTP(config.DEFAULT_SMTP_SERVER, config.DEFAULT_SMTP_PORT) as server:
            server.sendmail(sender, receiver, text)
