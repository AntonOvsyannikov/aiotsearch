from aiohttp import web

from .api import routes


# noinspection PyUnusedLocal
def get_app(argv):
    app = web.Application()
    app.add_routes(routes)
    return app
