#
# override config parameters here
#


config = {
    # database uri
    "SQLALCHEMY_DATABASE_URI" : "sqlite:///site.db",
    # url prefix for static content
    "STATIC_PREFIX" : "/static/",
    # url prefix for main site
    "SITE_PREFIX": "/",
    # title of the site
    "SITE_TITLE": "pytracker"
}
