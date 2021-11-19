import dash
from flask_sqlalchemy import SQLAlchemy

from config.gcp import AppConfig

app = dash.Dash(__name__)
app.server.config.from_object(AppConfig)
db = SQLAlchemy(app.server)

print("Init app")
