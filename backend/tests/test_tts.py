import base64
import pytest
from app.services.tts import TTSModule
import soundfile as sf

@pytest.fixture
def tts_module():
    """Fixture to create an instance of TTSModule."""
    return TTSModule()

def test_synthesize(tts_module):
    """Test the synthesize method of TTSModule."""
    # Define the input text
    input_text = "Hello, this is a test."

    # Call the synthesize method
    audio_base64 = tts_module.synthesize(input_text)

    # Check if the output is a valid base64 string
    assert isinstance(audio_base64, str), "Output should be a string"
    assert audio_base64.isascii(), "Output should be ASCII (base64 is ASCII)"

    # Optionally, check if the base64 string can be decoded back to bytes
    decoded_audio = base64.b64decode(audio_base64)
    assert isinstance(decoded_audio, bytes), "Decoded output should be bytes"

    sf.write("speech.wav", decoded_audio, samplerate=16000)

# To run the tests, use the command:
# pytest test_tts.py
