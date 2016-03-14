from . import torrent
from . import models
from . import query

def generateSearchKeywords(session, text):
    if isinstance(text, str):
        text = text.split()
    yield from query.filterCommonWords(session, text)

def handleUpload(session, request):
    """
    handle upload request
    """
    catno = request.form['cat']
    # assume this doesn't go bad
    cat = session.query(models.Category).filter(models.Category.cat_id == catno).limit(1).first()

    description = request.form['desc']

    # load torrent
    f = request.files['torrent']
    # parse torrent
    tdict = torrent.parseTorrent(f)
    # validate torrent
    if torrent.validate(tdict):
        # generate infohash
        infohash = torrent.infohash_hex(tdict)
        # check for duplicate
        if query.hasTorrentByInfoHash(session, infohash):
            # we already have this torrent
            return None, None, 'torrent already uploaded'
        # add torrent
        t = models.Torrent(tdict, description)
        session.add(t)
        session.commit()
        files = list()
        info = tdict[b'info']
        # add file records
        if b'files' in info:
            # many files
            for f in info[b'files']:
                session.add(models.TorrentFile(f, t.t_id))
                files.append(torrent.getFileName(f))
        else:
            # one file
            session.add(models.TorrentFile(info, t.t_id))
            files.append(torrent.getFileName(info))
        # generate keywords from description
        for keyword in generateSearchKeywords(session, description):
            session.add(models.SearchResult(t, cat, keyword))
        # generate keywords from files
        for keyword in generateSearchKeywords(session, ' '.join(files)):
            session.add(models.SearchResult(t, cat, keyword))
        session.commit()
        return t, tdict, None
    return None, None, "invalid torrent file"
