# project/server/__main__.py

# === Import(s) ===
# => Local <=
from project.server import create_app

# => System <=
import os

# === Set Configs ===
os.environ["APP_SETTINGS"] = "project.server.LocalDevConfig"

# === Run A Single-Instance Application ===
app = create_app()
app.run(debug=True)
