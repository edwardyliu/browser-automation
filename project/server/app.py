# project/server/app.py

# === Import(s) ===
# => System <=
import os

# => External <=
from flask import Flask
from flask_cors import CORS

# === Flask Application ===
def create_app()->Flask:
    """Create & return a Flask app instance

    Returns
    -------
    Flask
    """
    
    # instantiate the app
    app = Flask(__name__)
    CORS(app)

    # set configs
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # register blueprints
    from project.server.views import site
    from project.server.views import api
    
    app.register_blueprint(site)
    app.register_blueprint(api, url_prefix="/api")

    # shell context for flask cli
    app.shell_context_processor( {"app": app} )

    return app
