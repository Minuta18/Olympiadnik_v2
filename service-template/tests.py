import main
import app
import pytest
import httpx
import asyncio

client = httpx.AsyncClient(app=main.my_app, base_url=f'http://127.0.0.1:17012{app.PREFIX}')

@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()