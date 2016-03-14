from flask.ext.sqlalchemy import get_debug_queries

def fullSiteURL(app, *args):
    """
    generate the full url for a resource on the site
    """
    if not isinstance(args, str):
        args = '/'.join(args)
    return 'http://{}{}{}'.format(app.config['SITE_ADDR'], app.config['SITE_PREFIX'], args)
