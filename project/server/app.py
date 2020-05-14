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
    app = Flask(
        __name__,
        # static_folder="./build/static",
        # template_folder="./build"
    )
    CORS(app)

    # set configs
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # register blueprints
    from . import views
    
    # app.register_blueprint(views.static)
    app.register_blueprint(views.api, url_prefix="/api")

    # shell context for flask cli
    app.shell_context_processor( {"app": app} )

    return app
