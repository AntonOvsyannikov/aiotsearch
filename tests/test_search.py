import pytest
from aiotsearch.app import get_app


@pytest.fixture
async def cli(aiohttp_client):
    app = get_app([])
    return await aiohttp_client(app)


async def test_end_to_end(cli):
    response = await cli.post('/topics', json=[
        {'topic_name': "новости",
         'topic_data': ["деревья на Садовом кольце", "добрый автобус", "выставка IT-технологий"]},

        {'topic_name': "кухня",
         'topic_data': ["рецепт борща", "яблочный пирог", "тайская кухня"]},

        {'topic_name': "товары",
         'topic_data': ["Дети капитана Гранта", "зимние шины", "Тайская кухня"]},
    ])

    assert response.status == 200
    assert await  response.json() == ["новости", "кухня", "товары"]

    response = await cli.get('/search', params={'text': "где купить зимние шины"})
    assert response.status == 200
    assert set(await  response.json()) == {"товары"}

    response = await cli.get('/search', params={'text': "борща любимого рецепт"})
    assert response.status == 200
    assert set(await  response.json()) == {"кухня"}

    response = await cli.get('/search', params={'text': "тайская кухня"})
    assert response.status == 200
    assert set(await  response.json()) == {"кухня", "товары"}

    response = await cli.get('/search', params={'text': "кухня"})
    assert response.status == 200
    assert set(await  response.json()) == set()
