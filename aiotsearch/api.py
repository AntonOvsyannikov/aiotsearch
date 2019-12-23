# noinspection PyUnresolvedReferences
import json
import logging

from aiohttp import web


# ===========================================

def log(*args, **kwargs):
    logging.getLogger('aiohttp.server').debug(*args, **kwargs)


# ===========================================

def tokenize(phrase) -> set:
    return set(map(lambda s: s.lower(), phrase.split(' ')))


# ===========================================

routes = web.RouteTableDef()


async def init_app(app):
    app['topics'] = {}


@routes.post('/topics')
async def add_topic(request):
    topics = await request.json()
    result = []

    for topic in topics:
        topic_name = topic['topic_name']
        topic_data = topic['topic_data']

        request.app['topics'][topic_name] = request.app['topics'].get(topic_name, [])

        for phrase in topic_data:
            request.app['topics'][topic_name].append(tokenize(phrase))

        result.append(topic_name)

    return web.json_response(result)


@routes.get('/search')
async def search(request):
    text = tokenize(request.query['text'])
    topics = []

    def is_in_topic(text, phrases):
        for phrase in phrases: # type: set
            if phrase - text == set():
                return True
        return False

    for topic, phrases in request.app['topics'].items():
        if is_in_topic(text, phrases):
            topics.append(topic)

    return web.json_response(topics)
