#
# server routes
#

import flask
from .server import app, db
from . import models
from . import search
from . import util

import time

def render_template(name, **kwargs):
    """
    wraps flask.render_template, injects application variables
    """
    # inject prefixes
    kwargs["site_prefix"] = app.config["SITE_PREFIX"]
    kwargs["static_prefix"] = app.config["STATIC_PREFIX"]
    kwargs["debuginfo"] = util.get_debug_queries()
    # now do the render dance !
    return flask.render_template(name, **kwargs)

@app.route("/")
def serveIndex():
    """
    serve front page
    """
    return render_template('index.html', title="Search")


@app.route("/css/dynamic.css")
def serveDynamicCSS():
    """
    serve dynamically generated stylesheets
    used for injecting prefix into stylesheets
    """
    @flask.after_this_request
    def after(response):
        response.headers['Content-Type'] = 'text/css'
        return response
    return render_template("dynamic.css")

@app.route('/upload', methods=['GET', 'POST'])
def handleUpload():
    if flask.request.method.lower() == 'get':
        cats = db.session.query(models.Category).all()
        return render_template('upload.html', cats=cats, title="upload")
    return 'dix'

@app.route('/search')
def handleSearchQuery():
    args = flask.request.args
    terms = args.get('q', '')
    start = time.time()
    search_result = search.find(db.session, args)
    results = list()
    for res in search_result:
        results.append(res)
    dlt = time.time() - start
    return render_template("search_results.html", results=results, terms=terms, time=round(dlt, 2), title="search")
