# Quick Start: Docker Development Environment
## Requirements:
```bash
docker 19.03.6
docker-compose 1.25.5
```

## Run:
```bash
$ bash nauto.sh --make Chrome
$ docker-compose up -d --build
```

# Quick Start: Openshift
## Convert:
```bash
$ kompose convert -f docker-compose.yml --provider=openshift
```

## Up:
```bash
$ bash nauto.sh --make Chrome
$ kompose -f docker-compose.yml --provider=openshift up
```

# Quick Start: Local Development Environment
## Requirements:
```bash
OS: Linux

npm 6.14.5       => React (Front-End)
python 3.6.10    => Flask (Back-End)
```

## Run:
```bash
$ pip install -r ./project/server/requirements.txt
$ bash nauto.sh --make
```

### Serve Local SMTP Server
```bash
$ python -m smtpd -n -c DebuggingServer 127.0.0.1:25
```

### Serve Local Redis Server
```bash
$ redis-server
```

### Serve Local Redis Worker(s)
```bash
$ rq worker
```

### Serve Python Flask Application
```bash
$ python -m project.server
```
