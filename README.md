# Requirements:
```bash
OS: Linux

npm 6.14.5      => React (Front-End)
python 3.7.7    => Flask (Back-End)
```

# Setup:
```bash
$ pip install -r ./project/server/requirements.txt
$ bash nauto.sh --make
```

# Quick Start: Local Development Environment
## 1. Serve a Redis Server
```bash
$ redis-server
```

## 2. Serve Redis Worker(s)
```bash
rq worker
```

## 3. Serve an SMTP Server
```bash
$ python -m smtpd -n -c DebuggingServer 127.0.0.1:1025
```

## 4. Run Flask Application
```bash
$ python -m project.server
```
