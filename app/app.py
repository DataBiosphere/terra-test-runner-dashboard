import dash

from database.models import db
from config.gcp import AppConfig


def start(name=__name__):
    app = dash.Dash(name)
    app.server.config.from_object(AppConfig)
    db.init_app(app.server)
    return app
