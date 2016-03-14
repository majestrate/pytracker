#
# override config parameters here
#

import os

config = {
    # database uri
    "SQLALCHEMY_DATABASE_URI" : "sqlite:////tmp/site.db",
    # url prefix for static content
    "STATIC_PREFIX" : "/static/",
    # url prefix for main site
    "SITE_PREFIX": "/",
    # title of the site
    "SITE_NAME": "pytracker",
    # enable debug mode?
    "DEBUG": False,
    # app secret key goes here
    "SECRET_KEY": os.urandom(8),
    # upload directory
    "UPLOAD_DIR": "/tmp/uploads"
}
