# project/server/tasks/ina/job.py

# === Import(s) ===
# => Local <=
from . import utils
from . import config
from . import models
from . import driver
from . import template

# => System <=
import os
import re
import uuid
import smtplib
import datetime
from collections import deque
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Object Definition ===
class Job(object):
    """ Define a Job Object

    A list of Tasks objects
    """

    def __init__(self, uid:str=None, browser:str=None):
        self.id = uid or str(uuid.uuid4())
        self.log = utils.get_logger(f"INA.Job.{self.id}")
        self.dt = datetime.datetime.now()

        self.browser = browser
        self.driver = None
        self.queue = deque([])
        self.lines = []

    def __del__(self):
        if self.driver: del self.driver
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
    
    # === Setter(s) ===
    def reset(self):
        """Reset Task list

        """

        self.queue.clear()
        self.lines.clear()

    # === Functional ===
    def push(self, task:models.Task, fmt:str=None, elut:dict=None, trace:bool=True):
        """Enqueue new Task object

        Parameters
        ----------
        task: models.Task
            The Task object
        fmt: str, optional
            The string format
        elut: dict, optional
            An external lookup table
        trace: bool, optional
            If 'lines' will be appended
        """

        self.queue.append((task, fmt, elut, trace))
    
    def pop(self):
        """Dequeue (i.e. assign & exec) the oldest Task object

        """
        
        task, fmt, elut, trace = self.queue.popleft()
        if task:
            if task.key != self.driver.taskkey(): 
                self.driver.assign(task)
            else: 
                self.driver.reset()
            ilut = self.driver.exec(elut)

            if trace:
                if fmt: 
                    line = self.task2str(fmt, elut, ilut)
                else: 
                    line = self.task2str(config.DEFAULT_FORMAT, elut, ilut)
                self.lines.append(line)
    
    def deploy(self, receipt:str=None):
        """Pop until the queue is empty and then notify the <receipt>

        """

        if len(self.queue) > 0:
            if not self.driver: 
                self.driver = driver.Driver(self.id, browser=self.browser)
            
            while len(self.queue) > 0: self.pop()
            if receipt: self.notify(receipt)

    # === Utility Function(s) ===
    def task2str(self, fmt:str, elut:dict, ilut:dict)->str:
        """Parse the Task response to a formatted string

        Parameters
        ----------
        fmt: str
            The string format
        elut: dict
            An external look-up table
        ilut: dict
            An internal look-up table

        Returns
        -------
        str: The formatted string
        """

        for placeholder in re.findall(config.RE_POSITIONAL, fmt):
            value = placeholder[2:-1]
            if value == config.LUTV: 
                span = []
                for i, j in elut.items(): span.append(f"{i}: {j}")
                fmt = fmt.replace(placeholder, ", ".join(span))

            elif value == config.ARGV: fmt = fmt.replace(placeholder, ", ".join(ilut.values()))
            elif value == config.LAST: fmt = fmt.replace(placeholder, ilut.get(list(ilut.keys())[-1], "N/A"))
            elif value.isdigit(): fmt = fmt.replace(placeholder, ilut.get(placeholder, "N/A"))
            else: 
                if isinstance(elut, dict): fmt = fmt.replace(placeholder, elut.get(value, "N/F"))
                else: fmt = fmt.replace(placeholder, "N/F")
        
        return fmt

    def ig(self, lst:list, idx:int):
        """Safe Index Get

        Parameters
        ----------
        lst: list
            A list of objects
        idx: int
            An index
        """

        try: return lst[idx]
        except IndexError: return "N/A"

    def make_attachment(self, path:str):
        """Make an E-mail attachment via the file fetched from <path>

        Parameters
        ----------
        path: str
            The file path

        Returns
        -------
        MIMEBase
        """

        # Open the file in binary mode
        with open(path, "rb") as attachment:
            # Add file as application/octet-stream
            # Most E-mail client can download this automatically as an attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode the file to ASCII characters for sending via E-mail    
        encoders.encode_base64(part)

        # Add header as key-value pair to the attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(path)}",
        )
        
        return part

    def send_email(self, receipt:str, attachment=None):
        """Send <receipt> an e-mail w/ <attachment>
        
        Parameters
        ----------
        receipt: str
            An e-mail address
        attachment: MIMEBase
            A file attachment
        """

        sender = config.DEFAULT_SENDER_EMAIL

        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receipt
        message["Subject"] = "Nauto Report"

        # === Build HTML Content ===
        body = template.body_meta(taskid=self.id, dt=self.dt)
        body += template.body_information(email=sender)
        body += template.body_content_head("User ID", "Env", "Name", "Order ID")
        if len(self.lines) > 0:
            lastrow = self.lines[-1].split(",")
            for line in self.lines[:-1]:
                row = line.split(",")
                body += template.body_content_item(
                    self.ig(row, 0), self.ig(row, 1), 
                    self.ig(row, 2), self.ig(row, 3), False
                )
            body += template.body_content_item(
                self.ig(lastrow, 0), self.ig(lastrow, 1), 
                self.ig(lastrow, 2), self.ig(lastrow, 3), True
            )
        body += template.body_content_summary(True)
        html = template.header + body + template.footer(email=sender)

        message.attach(MIMEText(template.text(True), "plain"))
        message.attach(MIMEText(html, "html"))

        # === Add The Attachment ===
        if attachment: message.attach(attachment)

        # === Send The E-mail ===
        text = message.as_string()
        with smtplib.SMTP(config.DEFAULT_SMTP_SERVER, config.DEFAULT_SMTP_PORT) as server:
            server.sendmail(sender, receipt, text)

    def notify(self, receipt:str):
        """Notify <receipt> of Job results

        Parameters
        ----------
        receipt: str
            An E-mail address
        """
        
        path = os.path.join(config.CACHE_DIRPATH, f"{self.id}.csv")
        utils.write(self.lines, path)
        attachment = self.make_attachment(path)
        self.send_email(receipt, attachment=attachment)
        utils.remove(path)
    