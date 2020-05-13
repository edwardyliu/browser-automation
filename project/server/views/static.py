# project/server/views/static.py

# == Import(s) ==
# => External <=
from flask import Blueprint, render_template

# === Flask Blueprint ===
static = Blueprint("static", __name__)

# => Route(s) <=
@static.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")
