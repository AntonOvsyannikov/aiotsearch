import os
import sys

from aiohttp import web

from .app import get_app

web.run_app(
    get_app(sys.argv),
    host=os.environ.get('APP_HOST', '0.0.0.0'),
    port=int(os.environ.get('APP_PORT', 8080)),
)
