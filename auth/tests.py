import main
import app
import pytest
import httpx
import asyncio
import datetime

client = httpx.AsyncClient(app=main.my_app, base_url=f'http://127.0.0.1:16110{app.PREFIX}')

@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_health_check():
    response = await client.get('auth/health')
    assert response.status_code == 200

    response_json = await response.json()
    assert response_json['error'] == False
    assert response_json['time'] == datetime.datetime.time(datetime.datetime.now())

# @pytest.mark.asyncio
# @pytest.mark.order(2)
# async def test_():
