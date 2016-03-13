#
# database models
#

from .server import db

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
    
    def __init__(self, infohash, description):
        """
        construct torrent given 40 byte infohash as hex with description
        """
        assert len(infohash) == 40
        self.infohash = infohash
        if description is None:
            description = 'No Description'
        self.description = description
        now = datetime.utcnow()
        self.uploaded = now
        self.updated = now
        
    def summary(self, truncate=500):
        """
        get short summary, truncate if too big
        """
        desc = self.description
        if len(desc) > truncate:
            desc = desc[:truncate] + '...'
        return desc


    def downloadURL(self):
        return '/download/{}.torrent'.format(self.t_id)

    def infoURL(self):
        return '/torrent/{}'.format(self.t_id)
    
class TorrentFile(db.Model):
    """
    a filename included in a torrent's meta info
    """
    __tablename__ = 'torrentfiles'
    # if of this entry
    id = db.Column(db.Integer, primary_key=True)
    # filename of a file
    filename = db.Column(db.Text)
    # size of the file in bytes
    filesize = db.Column(db.Integer)
    # the torrent's id
    torrent_id = db.Column(db.Integer, db.ForeignKey('torrents.t_id'))
    
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


class SearchTag(db.Model):
    """
    a keyword used in searching
    """

    __tablename__ = 'searchtags'
    
    tag_id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String, unique=True)
        
class SearchResult(db.Model):
    """
    pregenerated search results
    """
    __tablename__ = 'searchresults'

    id = db.Column(db.Integer, primary_key=True)
    # which torrent is matched in this result
    t_id = db.Column(db.Integer, db.ForeignKey('torrents.t_id'))
    # which category is matched with this result
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.cat_id'))
    # which search tag does this result match with
    tag_id = db.Column(db.Integer, db.ForeignKey('searchtags.tag_id'))


class CommonWord(db.Model):
    """
    common words to not include in search query keywords
    """

    __tablename__ = 'commonwords'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, unique=True)

