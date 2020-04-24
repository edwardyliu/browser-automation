# == Import(s) ==
# => System
import time

# => External
from flask import Flask

# == Application ==
app = Flask("__main__")

@app.route("/time")
def get_current_time():
    return {"time": time.time()}

app.run()
