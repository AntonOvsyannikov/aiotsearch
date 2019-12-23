from aiohttp import web

from .api import routes, init_app


# noinspection PyUnusedLocal
def get_app(argv):
    app = web.Application()
    app.on_startup.append(init_app)
    app.add_routes(routes)
    return app
