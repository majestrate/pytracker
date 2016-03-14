#
# database models
#

from .server import db
from . import torrent
import datetime
    
class Torrent(db.Model):
    """
    an uploaded torrent
    """

    __tablename__ = 'torrents'
    
    # internal id
    t_id = db.Column(db.Integer, primary_key=True)
    # the torrent infohash
    infohash = db.Column(db.String(40), unique=True)
    # when it was uploaded first
    uploaded = db.Column(db.DateTime)
    # when it was modified last
    updated = db.Column(db.DateTime)
    # description of torrent
    description = db.Column(db.Text)
    # title of the torrent
    title = db.Column(db.Text)
    
    def __init__(self, tdict, description):
        """
        construct torrent given 40 byte infohash as hex with description
        """
        infohash = torrent.infohash_hex(tdict)
        self.infohash = infohash
        
        if description is None:
            description = 'No Description'
        self.description = description

        self.title = torrent.torrentName(tdict)
        
        now = datetime.datetime.utcnow()
        self.uploaded = now
        self.updated = now

    def filename(self):
        """
        get filename for the corrisponding uploaded torrent file
        """
        return '{}-{}.torrent'.format(self.infohash, self.t_id)
    
    def summary(self, truncate=500):
        """
        get short summary, truncate if too big
        """
        desc = self.description
        if len(desc) > truncate:
            desc = desc[:truncate] + '...'
        return desc

    def magnet(self):
        return 'magnet:?xt=urn:btih:{}'.format(self.infohash)
    
    def downloadURL(self):
        return '/download/{}'.format(self.filename())

    def infoURL(self):
        return '/torrent/{}'.format(self.t_id)
    
class TorrentFile(db.Model):
    """
    a filename included in a torrent's meta info
    """
    __tablename__ = 'torrentfiles'

    def __init__(self, tdict, tid):
        self.filesize = torrent.getFileLength(tdict)
        self.filename = torrent.getFileName(tdict)
        self.torrent_id = tid
        
    # if of this entry
    id = db.Column(db.Integer, primary_key=True)
    # filename of a file
    filename = db.Column(db.Text)
    # size of the file in bytes
    filesize = db.Column(db.Integer)
    # the torrent's id
    torrent_id = db.Column(db.Integer, db.ForeignKey('torrents.t_id'))

    def prettySize(self):
        unit = 'B'
        size = self.filesize
        if self.filesize > 1024:
            unit = 'KB'
            size /= 1024.0
        if size > 1024:
            unit = 'MB'
            size /= 1024.0
        if size > 1024:
            unit = 'GB'
            size /= 1024.0
        return '{} {}'.format(round(size, 2), unit)
    
class Category(db.Model):
    """
    a category for torrents
    """

    __tablename__ = 'categories'
    
    cat_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        """
        create a new category with a name
        name must be unique
        """
        self.name = name
        
class SearchResult(db.Model):
    """
    pregenerated search results
    """
    __tablename__ = 'searchresults'

    def __init__(self, torrent, category, keyword):
        self.t_id = torrent.t_id
        self.cat_id = category.cat_id
        self.keyword = keyword
    
    id = db.Column(db.Integer, primary_key=True)
    # which torrent is matched in this result
    t_id = db.Column(db.Integer, db.ForeignKey('torrents.t_id'))
    # which category is matched with this result
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.cat_id'))
    # a keyword which matches this result
    keyword = db.Column(db.String)


class CommonWord(db.Model):
    """
    common words to not include in search query keywords
    """

    __tablename__ = 'commonwords'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, unique=True)

