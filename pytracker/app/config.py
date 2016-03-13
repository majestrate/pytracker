#
# override config parameters here
#


config = {
    # database uri
    "SQLALCHEMY_DATABASE_URI" : "sqlite:////tmp/site.db",
    # url prefix for static content
    "STATIC_PREFIX" : "/static/",
    # url prefix for main site
    "SITE_PREFIX": "/",
    # title of the site
    "SITE_NAME": "pytracker",
    "DEBUG": True,
}
