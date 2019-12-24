import logging


def log(*args, **kwargs):
    logging.getLogger('aiohttp.server').debug(*args, **kwargs)
