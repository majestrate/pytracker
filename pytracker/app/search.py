__doc__ = """
search engine
"""
from . import query

def randomQuery():
    """
    get a random query term from existing non-bad terms
    """
    return 'anime'

def removeBogons(word):
    """
    strip of bogon characters
    """
    res = ''
    for ch in word:
        if ch.isdigit() or ch.isalpha():
            res += ch
    return res


def find(session, args):
    """
    find 1 page of results given a search term
    yield results
    """
    # collect arguments
    keywords = args.get('q', '').split()
    category = args.get('c', None)
    page = args.get('p', 0, type=int)
    perpage = 10
    
    words = list()
    # filter bogus keyword parts
    for keyword in keywords:
        keyword = removeBogons(keyword)
        if keyword and len(keyword) > 0:
            words.append(keyword)
    # remove common keywords i.e. the, or, of
    keywords = list()
    for keyword in query.filterCommonWords(session, words):
        keywords.append(keyword)
    if len(keywords) > 0:
        # build search
        q = query.torrentsByKeywordAndCategory(session, keywords, category)
        # paginate
        q = query.paginate(q, page, perpage)
        # fetch torrent models
        q = query.torrentsById(session, q)
        # obtain
        yield from q.all()

