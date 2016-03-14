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
    # fqdn of site
    "SITE_ADDR" : "erkznua4l3dirxjo6qedjhiwnfj4dxk65azqddeu67jdgc3alw4q.b32.i2p",
    # title of the site
    "SITE_NAME": "pytracker",
    # enable debug mode?
    "DEBUG": True,
    # app secret key goes here
    "SECRET_KEY": os.urandom(8),
    # upload directory
    "UPLOAD_DIR": "/tmp/uploads",
    # do we force no js?
    "NOJS" : False
}
