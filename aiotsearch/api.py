# noinspection PyUnresolvedReferences
import json
import logging

from aiohttp import web


def log(*args, **kwargs):
    logging.getLogger('aiohttp.server').debug(*args, **kwargs)


routes = web.RouteTableDef()


@routes.get('/search')
async def get_search(request):
    text = request.query.get('text', None)
    if text is None:
        return web.json_response({'error': "Missing 'text' in query string"}, status=400)

    return web.json_response('hi')
