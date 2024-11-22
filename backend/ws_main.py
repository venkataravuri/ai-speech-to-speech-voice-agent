from fastapi import FastAPI, WebSocket
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.stt import stt_module
from app.services.audio_service import AudioService

app = FastAPI(debug=True)

@app.on_event("startup")
async def load_models():
    stt_module.load_model()
    # llm_module.load_model()
    # tts_module.load_model()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

audio_service = AudioService()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_text()
            response = await audio_service.process_audio_message(message)
            await websocket.send_text(response)
        except Exception:
            break

if __name__ == "__main__":
    uvicorn.run("ws_main:app", host="0.0.0.0", port=8000, reload=True, ws='websockets')