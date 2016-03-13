from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from .config import config

app = Flask(__name__)

# set config parameters
for k in config:
    app.config[k] = config[k]

db = SQLAlchemy(app)

