#
# server routes
#

import flask
from .server import app, db
from . import models
from . import search
from . import torrent
from . import upload
from . import util

import os
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
    cats = db.session.query(models.Category).all()
    if flask.request.method.lower() == 'post':
        form = flask.request.form
        files = flask.request.files
        t = None
        err = None
        res = None
        if 'torrent' not in files:
            err = "no torrent file included"
        elif 'cat' not in form:
            err = "no category selected"
        elif 'desc' not in form:
            err = "empty torrent description"
        else:
            # all good parsing
            res = upload.handleUpload(db.session, flask.request)
        if res:
            t, tdict, err = res
            if err is None:
                # save uploaded torrent
                with open(os.path.join(app.config["UPLOAD_DIR"], t.filename()), 'wb') as f:
                    torrent.dumpTorrent(tdict, f)
                flask.flash("uploaded {}".format(t.title))
                # we uploaded the torrent correctly
                return render_template("result.html", url=t.infoURL())
        # some error probably
        flask.flash("upload failed: {}".format(err))
        return render_template("result.html", url=flask.request.url)
    return render_template("upload.html", cats=cats, title="upload")

@app.route("/torrent/<int:tid>")
def serveTorrent(tid):
    session = db.session
    t = session.query(models.Torrent).filter(models.Torrent.t_id == tid).first()
    if t:
        files = session.query(models.TorrentFile).filter(models.TorrentFile.torrent_id == t.t_id).all()
        return render_template("torrent.html", torrent=t, files=files)
    flask.abort(404)

@app.route("/download/<path:fname>")
def serveDownload(fname):
    return flask.send_from_directory(app.config["UPLOAD_DIR"], fname, as_attachment=True)
    
@app.route('/search')
def handleSearchQuery():
    args = flask.request.args
    terms = args.get('q', '')
    start = time.time()
    results = search.find(db.session, args)
    dlt = time.time() - start
    return render_template("search_results.html", results=results, terms=terms, time=round(dlt, 2), title="search")
