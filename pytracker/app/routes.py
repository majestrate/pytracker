#
# server routes
#

import flask
from .server import app, db
from . import feed
from . import models
from . import query
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
    # inject force no js
    kwargs["nojs"] = app.config['NOJS']
    # now do the render dance !
    return flask.render_template(name, **kwargs)

@app.route("/")
def serveIndex():
    """
    serve front page
    """
    # get all categories
    cats = db.session.query(models.Category).all()
    # get last 10 torrents
    torrents = db.session.query(models.Torrent).order_by(models.Torrent.uploaded.desc()).limit(10)
    url = util.fullSiteURL(app, "feed", "all.rss")
    return render_template('index.html', title="Search", categories=cats, torrents=torrents, rss_url=url)


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

@app.route('/js/dynamic.js')
def serveDynamicJS():
    """
    serve dynamically generated js
    contains warning to force no js if configured to do so
    """
    @flask.after_this_request
    def after(response):
        response.headers["Content-Type"] = 'text/javascript'
        return response
    return render_template("dynamic.js")
    
@app.route('/upload', methods=['GET', 'POST'])
def handleUpload():
    """
    handle upload of torrent
    """
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
    """
    serve info page for a torrent
    """
    session = db.session
    t = session.query(models.Torrent).filter(models.Torrent.t_id == tid).first()
    if t:
        files = session.query(models.TorrentFile).filter(models.TorrentFile.torrent_id == t.t_id).all()
        return render_template("torrent.html", torrent=t, files=files)
    flask.abort(404)

@app.route("/download/<path:fname>")
def serveDownload(fname):
    """
    serve uploaded torrent
    """
    return flask.send_from_directory(app.config["UPLOAD_DIR"], fname, as_attachment=True)

@app.route("/feed/<cat>.<feedtype>")
def serveCategoryRSS(cat, feedtype):
    """
    serve rss feed for category
    if category is "all" get feed for all categories
    """
    limit = flask.request.args.get("l", 10, type=int)
    cat = cat.lower()
    if cat is 'all':
        cat = None
    q = query.torrentsByKeywordAndCategory(db.session, None, cat)
    q = query.torrentsById(db.session, q)
    q = query.paginate(q, 0, limit)
    feedtype = feedtype.lower()
    flask.response.headers['Content-Type'] = 'application/{}+xml'.format(feedtype)
    f = feed.generate(app, cat, q.all())
    if feedtype == 'rss':
        return f.rss_str()
    else:
        flask.abort(404)
    
@app.route("/cat/<cat>/<int:page>")
def serveCategoryPage(cat, page):
    """
    serve page for category
    """
    args = flask.request.args
    prev = None
    if page > 0:
        prev = flask.url_for('serveCategoryPage', cat=cat, page=page-1)
    next = flask.url_for('serveCategoryPage', cat=cat, page=page+1)
    start = time.time()
    q = query.torrentsByKeywordAndCategory(db.session, None, cat)
    q = query.torrentsById(db.session, q)    
    q = query.paginate(q, page, 10)
    torrents = q.all()
    dlt = time.time() - start
    if len(torrents) == 0:
        next = None
    return render_template("search_results.html", results=torrents, time=round(dlt, 2), title="browse torrents", category=cat, next_page=next, prev_page=prev, rss_url=util.fullSiteURL(app, 'feed', '{}.rss'.format(cat)))

@app.route('/search')
def handleSearch():
    return render_template("search.html")

@app.route('/search/<int:p>')
def handleSearchQuery(p):
    """
    handle search query
    """
    args = flask.request.args
    terms = args.get('q', '')
    prev = None
    if p > 0:
        prev = flask.url_for('handleSearchQuery', p=p-1)
    next = flask.url_for('handleSearchQuery', p=p+1)
    start = time.time()
    results = search.find(db.session, args)
    dlt = time.time() - start
    if len(results) == 0:
        next = None
    return render_template("search_results.html", results=results, terms=terms, time=round(dlt, 2), title="search", page=p)
