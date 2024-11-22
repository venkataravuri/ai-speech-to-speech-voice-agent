import json
import base64
from .stt import stt_module
from .llm import llm_module
from .tts import tts_module
from .memory import MemoryModule
from app.core.logging import logger

# Initialize modules
memory = MemoryModule()

class AudioService:
    async def process_audio_message(self, message_data: str) -> str:
        """Process incoming audio messages and return appropriate responses."""
        message = json.loads(message_data)

        if message["type"] == "audio":
            # Process audio data
            audio_bytes = base64.b64decode(message["content"])
            logger.info(f"{len(audio_bytes) = }")

            # Step 1: Convert audio to text
            user_input = stt_module.transcribe(audio_bytes)
            logger.info(f"{user_input = }")

            # Step 2: Add input to memory and retrieve context
            memory.add_context(user_input)
            context = memory.get_context()

            # Step 3: Generate LLM response
            response_text = None
            # response_text = llm_module.generate_response(user_input)

            # Step 4: Convert response to audio
            # audio_base64 = tts_module.synthesize(response_text)
            audio_base64 = None

            # Send transcription
            text_response = {
                "type": "text",
                "source": "user",
                "content": user_input
            }

            # Send AI response
            agent_response = {
                "type": "text",
                "source": "agent",
                "content": response_text
            }

            # Send TTS audio
            audio_response = {
                "type": "audio",
                "content": audio_base64
            }
            
            return json.dumps([text_response, agent_response, audio_response])
        
        return json.dumps({"error": "Unsupported message type"})