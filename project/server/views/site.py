# project/server/views/site.py

# == Import(s) ==
# => External <=
from flask import Blueprint, render_template

# === Flask Blueprint ===
site = Blueprint("site", __name__)

# => Route(s) <=
@site.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")
