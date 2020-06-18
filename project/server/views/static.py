# project/server/views/static.py

# == Import(s) ==
# => External <=
from flask import Blueprint, render_template, send_from_directory

# === Flask Blueprint ===
static = Blueprint("static", __name__)

# => Route(s) <=
@static.route("/home", methods=["GET"])
@static.route("/index", methods=["GET"])
@static.route("/static", methods=["GET"])
@static.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@static.route("/manifest.json")
def manifest():
    return send_from_directory('./build', 'manifest.json')

@static.route('/android-chrome-192x192.png')
def android_chrome_192():
    return send_from_directory('./build', 'android-chrome-192x192.png')

@static.route('/android-chrome-512x512.png')
def android_chrome_512():
    return send_from_directory('./build', 'android-chrome-512x512.png')

@static.route('/apple-touch-icon.png')
def apple_touch():
    return send_from_directory('./build', 'apple-touch-icon.png')

@static.route('/favicon.ico')
def favicon():
    return send_from_directory('./build', 'favicon.ico')

@static.route('/favicon-16x16.png')
def favicon_16():
    return send_from_directory('./build', 'favicon-16x16.png')

@static.route('/favicon-32x32.png')
def favicon_32():
    return send_from_directory('./build', 'favicon-32x32.png')

@static.route('/robots.txt')
def robots():
    return send_from_directory('./build', 'robots.txt')
