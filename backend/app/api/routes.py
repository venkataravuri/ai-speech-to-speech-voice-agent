from fastapi import APIRouter, WebSocket
from ..services.websocket_manager import ConnectionManager
from ..services.audio_service import AudioService
from ..core.logging import logger

router = APIRouter()
manager = ConnectionManager()
audio_service = AudioService()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        async for message in websocket.iter_text():
            response = await audio_service.process_audio_message(message)
            await websocket.send_text(response)
    except Exception as e:
        logger.error(f"Error in WebSocket endpoint: {e}")
    finally:
        await manager.disconnect(websocket)