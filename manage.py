# manage.py

# === Import(s) ===
# => Local <=
from project.server import create_app

# => External <=
import redis
from flask.cli import FlaskGroup
from rq import Connection, Worker

# === Flask Group Application ===
app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("run_worker")
def run_worker():
    with Connection(redis.from_url(app.config["REDIS_URL"])):
        worker = Worker(app.config["QUEUES"])
        worker.work()

if __name__ == "__main__":
    cli()
