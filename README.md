# Nauto:
A Browser Automation Tool Using Pre-Defined Finite State Machines

# Table of Contents:
1. [Quick Start](#quick-start)
    1. [Docker Build](#docker-build)
    1. [Local Build](#local-build)
1. [Requirements](#requirements)
1. [Credits](#credits)

# Quick Start:
## Docker Build
1. Requirements
    ```bash
    docker 19.03.6
    docker-compose 1.25.5
    npm 6.14.5
    ```

1. Setup
    ```bash
    $ bash nauto.sh --make Chrome
    ```

1. Start
    ```bash
    $ docker-compose up -d --build
    ```

## Local Build
1. Requirements
    ```bash
    npm 6.14.5
    python 3.6.10
    ```

1. Setup
    ```bash
    $ pip install -r ./project/server/requirements.txt
    $ bash nauto.sh --make FireFox
    ```

1. Start
    1. Local SMTP Server
        ```bash
        $ python -m smtpd -n -c DebuggingServer 127.0.0.1:25
        ```

    1. Local Redis Server
        ```bash
        $ redis-server
        ```

    1. Local Flask Server
        ```bash
        $ python -m project.server
        ```

    1. Local Redis Workers
        ```bash
        $ rq worker
        ```

# Requirements:
npm 6.14.5
```javascript
"@material-ui/core": "^4.9.14",
"@material-ui/icons": "^4.9.1",
"@material-ui/lab": "^4.0.0-alpha.53",

"autosuggest-highlight": "^3.1.1",
"axios": "^0.19.2",
"file-saver": "^2.0.2",
"papaparse": "^5.2.0",
"react": "^16.13.1",
"react-dom": "^16.13.1",
"react-scripts": "3.4.1",
"react-table": "^7.0.5"
```

Python 3.6.10
```python
dataclasses==0.7
Flask==1.1.2
Flask-Cors==3.0.8
pytz==2019.3
redis==3.5.1
rq==1.4.0
selenium==3.141.0
```

# Credits
* [Edward Y. Liu](edwardy.liu@mail.utoronto.ca)