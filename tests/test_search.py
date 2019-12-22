import pytest
from aiotsearch.app import get_app


@pytest.fixture
async def cli(aiohttp_client):
    app = get_app([])
    return await aiohttp_client(app)


async def test_hi(cli):
    response = await cli.get('/search', params = {'text':'test test'} )
    assert response.status == 200
    hi = await response.json()
    assert hi == "hi"
