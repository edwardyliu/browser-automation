# project/server/config.py

# === Configuration(s) ===
# => Local Config(s) <=
class BaseLocalConfig(object):
    """Define The Base Local Configuration Object

    The Localized Flask Application Configuration Object
    """

    WTF_CSRF_ENABLED = True
    REDIS_URL = "redis://127.0.0.1:6379/0"
    QUEUES = ["default"]

class LocalTestingConfig(BaseLocalConfig):
    """Define The Localized Testing Environment

    """

    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class LocalDevConfig(BaseLocalConfig):
    """Define The Localized Development Environment
    
    """

    WTF_CSRF_ENABLED = False

# => Docker Config(s) <=
class BaseDockerConfig(object):
    """Define The Base Docker Configuration Object

    The Dockerized Flask Application Configuration Object
    """

    WTF_CSRF_ENABLED = True
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]

class DockerTestingConfig(BaseDockerConfig):
    """Define The Dockerized Testing Environment

    """

    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class DockerDevConfig(BaseDockerConfig):
    """Define The Dockerized Development Environment

    """

    WTF_CSRF_ENABLED = False
    