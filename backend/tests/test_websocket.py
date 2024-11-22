import pytest
from websockets import ConnectionClosed, connect
import websockets

@pytest.fixture
async def client():
    async with connect("ws://127.0.0.1:8000/ws") as ws:
        yield ws

@pytest.mark.asyncio
async def test_websocket_ping(client):
    await client.send("ping")
    response = await client.recv()
    assert response == "pong"

# @pytest.mark.asyncio
# async def test_websocket_message(client):
#     await client.send("Hello, world!")
#     response = await client.recv()
#     assert response == "Received message: Hello, world!"

# @pytest.mark.asyncio
# async def test_websocket_disconnect(client):
#     await client.close()
#     with pytest.raises(ConnectionClosed):
#         await client.recv()