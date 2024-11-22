import pytest
from websockets import connect
import librosa
import base64
import json

@pytest.fixture
async def client():
    async with connect("ws://localhost:8000/ws") as ws:
        yield ws

@pytest.mark.asyncio
async def test_websocket_ping(client):

    # Load the audio file
    audio_file = "data/you-got-it-1.wav"

    # audio_segment = AudioSegment.from_wav(audio_file)

    # Set the language to English
    # language = "en"
    # convert to expected format
    # if audio_segment.frame_rate != 16000: # 16 kHz
    #     audio_segment = audio_segment.set_frame_rate(16000)
    # if audio_segment.sample_width != 2:   # int16
    #     audio_segment = audio_segment.set_sample_width(2)
    # if audio_segment.channels != 1:       # mono
    #     audio_segment = audio_segment.set_channels(1)       

    # print(type(audio_segment.get_array_of_samples()), len(audio_segment.get_array_of_samples())) 

    # arr = np.array(audio_segment.get_array_of_samples())
    # arr = arr.astype(np.float32)/32768.0

    audio, sr = librosa.load(audio_file, sr=16000)

    audio_base64 = base64.b64encode(audio).decode("utf-8")

    payload = {
          'type': 'audio',
          'content': audio_base64,
    }

    payload_json = json.dumps(payload)

    await client.send(payload_json)

    response = await client.recv()
    print(f"{response =}")

    await client.close()

    assert response == "pong"
