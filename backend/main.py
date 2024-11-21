from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import logger
from app.services.stt import stt_module
from app.services.llm import llm_module
from app.services.tts import tts_module

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

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

app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
