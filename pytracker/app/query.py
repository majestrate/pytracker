__doc__ = """
search engine
"""
from . import models

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
            cat_q = session.query(models.Category).filter(models.Category.name == category)
    if keywords and len(keywords) > 0:
        # keywords specified
        # check tags
        keywords_q = session.query(models.SearchTag.tag_id).filter(models.SearchTag.keyword.in_(keywords))
        
    result_q = session.query(models.SearchResult, models.SearchResult.t_id)
    
    # apply category filter query
    if cat_q:
        result_q = result_q.filter(models.SearchResult.cat_id.in_(cat_q))

    # apply keyword filter query
    if keywords_q:
        result_q = result_q.filter(models.SearchResult.tag_id.in_(keywords_q))
    
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
    return ids.correlate(session.query(models.Torrent))

def paginate(q, page, perpage):
    """
    apply pagination on a query
    """
    offset = page * perpage
    return q.offset(offset).limit(perpage)


def filterCommonWords(session, keywords):
    """
    filter out common keywords from a list of keywords
    yield filtered words
    """
    words = dict()
    # collect keywords into a dict of unique words
    for word in keywords:
        # only do words with more than 3 words
        if len(word) > 3:
            if word not in words:
                words[word] = 0
            words[word] += 1

    # find all common words in the unique keywords
    unique_keywords = words.keys()
    q = session.query(models.CommonWord).filter(models.CommonWord.word.in_(unique_keywords))
    # filter out common keywords found
    for res in q:
        del words[res.word]

    # yield remaining keywords
    for keyword in words:
        yield keyword
           
    
