from aiohttp import web

from .search import Search

routes = web.RouteTableDef()


async def init_app(app):
    app['search'] = Search()


@web.middleware
async def middleware(request, handler):
    try:
        result = await handler(request)
    except Search.StateError as e:
        return web.json_response({'error': str(e)}, status=422)
    # except Exception as e:
    #     return web.json_response({'error': str(e)}, status=400)
    return result


@routes.post('/topics')
async def add_topic(request):
    search: Search = request.app['search']
    topics = await request.json()
    return web.json_response(
        await search.add_topics([(t['topic_name'], t['topic_data']) for t in topics])
    )


@routes.post('/commit')
async def commit(request):
    search: Search = request.app['search']
    await search.commit()
    return web.Response()


@routes.get('/search')
async def search(request):
    search: Search = request.app['search']
    return web.json_response(
        await search.search(request.query['phrase'])
    )
