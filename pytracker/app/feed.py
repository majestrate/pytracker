from feedgen.feed import FeedGenerator

from . import util

def generate(app, category, torrents):
    """
    generate an rss feed from category with torrents as results
    if category is None this feed is for all categories
    """
    feed = FeedGenerator()
    if category:
        url = util.fullSiteURL(app, 'feed', '{}.rss'.format(category))
    else:
        url = util.fullSiteURL(app, 'feed', 'all.rss')
    feed.link(href=url, rel="self")
    feed.id(url)
    if category:
        title = "new {} torrents on index ex invisibilis".format(category)
    else:
        title = "new torrents on index ex invisibilis"
    feed.title(title)
    feed.description(title)
    feed.author({"name": "anonymous"})
    feed.language("en")
    for torrent in torrents:
        item = feed.add_entry()
        url = util.fullSiteURL(app, torrent.downloadURL())
        item.id(torrent.infohash)
        item.link(href=url)
        item.title(torrent.title)
        item.description(torrent.summary(100))
    return feed
