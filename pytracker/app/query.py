__doc__ = """
search engine
"""
from . import models

import string

def torrentsByKeywordAndCategory(session, keywords, category):
    """
    build query that gets torrent ids given a category name and a list of keywords that matches to it
    """
    print('keywords: {} category: {}'.format(keywords, category))
    keywords_q = None
    cat_q = None
    if category is not None:
        if isinstance(category, str):
            # get category by name
            cat_q = session.query(models.Category.cat_id).filter(models.Category.name == category)

    result_q = session.query(models.SearchResult.t_id)
    
    # apply category filter query
    if cat_q:
        result_q = result_q.filter(models.SearchResult.cat_id.in_(cat_q))

    # apply keyword filter query
    if keywords and len(keywords) > 0:
        result_q = result_q.filter(models.SearchResult.keyword.in_(keywords))
        
    return result_q
    
        
def torrentsByOlder(q):
    """
    build query that selects older torrents first using an existing query that selects torrent ids
    """
    return q.order_by(models.Torrent.uploaded.asc())

def torrentsByNewer(q):
    """
    build a query that selects newer torrents first using an existing query that selects torrent ids
    """
    return q.order_by(models.Torrent.uploaded.desc())

def torrentsById(session, ids):
    """
    build a query that gets torrent models given their ids
    """
    return session.query(models.Torrent).filter(models.Torrent.t_id.in_(ids))

def paginate(q, page, perpage):
    """
    apply pagination on a query
    """
    offset = page * perpage
    return q.offset(offset).limit(perpage)

def hasTorrentByInfoHash(session, infohash):
    """
    return true if we already have a torrent given its infohash
    return false if we don't have a torrent with this infohash
    """
    return session.query(models.Torrent).filter(models.Torrent.infohash == infohash).count() > 0

def filterCommonWords(session, keywords):
    """
    filter out common keywords from a list of keywords
    yield filtered words
    """
    words = dict()
    # collect keywords into a dict of unique words
    for word in keywords:
        # split up via punctuation
        for ch in string.punctuation:
            word = word.replace(ch, ' ')
        # only do words with more than 3 words
        word = word.lower()
        for w in word.split():
            if len(w) > 2:
                if w not in words:
                    words[w] = 0
                words[w] += 1

    # find all common words in the unique keywords
    unique_keywords = words.keys()
    q = session.query(models.CommonWord).filter(models.CommonWord.word.in_(unique_keywords))
    # filter out common keywords found
    for res in q:
        del words[res.word]

    # yield remaining keywords
    for keyword in words:
        yield keyword
           
    
