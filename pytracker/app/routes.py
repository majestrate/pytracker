#
# server routes
#

import flask
from .server import app
from . import models


def render_template(name, **kwargs):
    """
    wraps flask.render_template, injects application variables
    """
    # inject prefixes
    kwargs["site_prefix"] = app.config["SITE_PREFIX"]
    kwargs["static_prefix"] = app.config["STATIC_PREFIX"]
    # now do the render dance !
    return flask.render_template(name, **kwargs)

@app.route("/")
def serveIndex():
    return render_template('index.html', title=app.config["SITE_TITLE"])
