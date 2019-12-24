from aiohttp import web

from .api import routes, init_app, middleware

def get_app():
    app = web.Application(middlewares=[middleware])
    app.on_startup.append(init_app)
    app.add_routes(routes)
    return app
