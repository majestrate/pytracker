from pytracker.app import server
from pytracker.app import routes
from pytracker.app import models


def run(*args, **kwargs):
    """
    run app server
    all parameters are passed into flask app
    """
    server.app.run(*args, **kwargs)

def seed():
    """
    seed with initial data
    """
    server.db.create_all()
    session = server.db.session

    # initial categories
    cats = ['anime', 'leaks', 'books', 'apps', 'misc', 'movies', 'tv']
    for cat in cats:
        c = models.Category(cat)
        session.add(c)
    # commit
    session.commit()

def nuke():
    """
    drop all tables
    """
    server.db.drop_all()
    
