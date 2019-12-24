import pytest
from aiotsearch.app import get_app


@pytest.fixture
async def cli(aiohttp_client):
    app = get_app()
    return await aiohttp_client(app)


async def test_end_to_end(cli):
    # ============== Topics

    response = await cli.post('/topics', json=[
        {'topic_name': "новости",
         'topic_data': ["деревья на Садовом кольце", "добрый автобус", "выставка IT-технологий"]},

        {'topic_name': "кухня",
         'topic_data': ["рецепт борща", "яблочный пирог", "тайская кухня"]},
    ])

    assert response.status == 200
    assert await response.json() == ["новости", "кухня"]

    response = await cli.post('/topics', json=[
        {'topic_name': "товары",
         'topic_data': ["Дети капитана Гранта", "зимние шины", "Тайская кухня"]},
    ])

    assert response.status == 200
    assert await response.json() == ["товары"]

    # Test "not commited" error. Commit should be issued before proceeding searches.
    # This is just for simplicity of synchronization on server side
    response = await cli.get('/search', params={'phrase': "где купить зимние шины"})
    assert response.status == 422

    response = await cli.post('/commit')
    assert response.status == 200

    # Topic posting is not available anyhmore after commit
    response = await cli.post('/topics', json=[
        {'topic_name': "товары",
         'topic_data': ["Дети капитана Гранта", "зимние шины", "Тайская кухня"]},
    ])
    assert response.status == 422

    # ============== Searches

    response = await cli.get('/search', params={'phrase': "где купить зимние шины"})
    assert response.status == 200
    assert set(await response.json()) == {"товары"}

    response = await cli.get('/search', params={'phrase': "борща любимого рецепт"})
    assert response.status == 200
    assert set(await response.json()) == {"кухня"}

    response = await cli.get('/search', params={'phrase': "тайская кухня"})
    assert response.status == 200
    assert set(await response.json()) == {"кухня", "товары"}

    response = await cli.get('/search', params={'phrase': "кухня"})
    assert response.status == 200
    assert set(await response.json()) == set()
