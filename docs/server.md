# Server - Tasks:
A Module Designated to Serve Various Backend API Requests.
<br>
It contains a set of pre-defined Task objects constructed via JSON files read from "journal/*.json"

# Table of Contents:
1. [Description](#description)
    * [utils.py](#file-utils.py)
    * [config.py](#file-config.py)
    * [APIs: tasks.py](#file-tasks.py)
1. [Requirements](#requirements)
1. [Usage](#usage)
1. [Credits](#credits)

# Description:
## File utils.py
```python
def json2task()->ina.Task:
    """Construct an INA Task Object via JSON

    Required JSON Format:
    {
        "name": <INA.Key.name>
        "env: <INA.Key.env>
        "commands": [
            [<INA.Command.label>, {
                "target": <INA.Command.target>,
                "argv": <INA.Command.argv>
            }], 
            
            ...
        ]
    }
    """

def get_task_dict()->dict:
    """Get 'dict' of Task Objects via JSONs from "journal/*.json"
    
    Keys are respective INA.Key objects
    """
```

## File config.py
Define a sequence of INA Commands to be executed before and after each INA Task:
```python
# Before each Task
PREFIX=[
    ina.Command(
        label="GET",
        target="https://www.google.com/",
        argv=None
    ),

    ...
]

# After each Task
SUFFIX=[
    ina.Command(
        label="PRINTF",
        target="Task Complete :)",
        argv=None
    ),

    ...
]
```

## File tasks.py
Available Tasks API
```python
def keys()->list:
    """Get a List of Available INA.Key Values

    """

def create_scan()->bool:
    """Create & Deploy an INA.Job Instance

    Custom Job: Scan
    """

def create_job()->bool:
    """Create & Deploy an INA.Job Instance

    """
```

# Requirements:
Python 3.6.10
```python
dataclasses==0.7
pytz==2019.3
selenium==3.141.0
```

# Usage:
* Simple Use-Case
    ```python
    import tasks

    tasks_keys = tasks.keys()
    print(f"Available Keys: {tasks_keys}")

    job_status = tasks.create_job(
        {
            "receipt": "edwardy.liu@mail.utoronto.ca",
            "data": [
                {
                    "usrId": "Edward",
                    "env": "TEST",
                    "name": "TEST ALL",
                    "lut": ""
                },
                {
                    "usrId": "Han",
                    "env": "TEST",
                    "name": "TEST PRINTF",
                    "lut": ""
                }
            ]
        },
        uid="UniqueID",
        browser="FireFox"
    )
    print(f"Job Status: {job_status}")
    ```

# Credits:
* [Edward Y. Liu](edwardy.liu@mail.utoronto.ca)