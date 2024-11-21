import base64
import json
import pytest
from websockets import connect
import pydub
import io

@pytest.fixture
async def client():
    async with connect("ws://localhost:8000/api/ws") as ws:
        yield ws


@pytest.mark.asyncio
async def test_api(client):

    wav_file = pydub.AudioSegment.from_file("data/female-vocal-321-countdown-240912.mp3", format="mp3")


    # data type for the file
    print(type(wav_file))
    # OUTPUT: <class 'pydub.audio_segment.AudioSegment'>

    # To find frame rate of song/file
    print(wav_file.frame_rate)
    # OUTPUT: 22050

    # To know about channels of file
    print(wav_file.channels)
    # OUTPUT: 1

    # Find the number of bytes per sample
    print(wav_file.sample_width )
    # OUTPUT : 2


    # Find Maximum amplitude
    print(wav_file.max)
    # OUTPUT 17106

    # To know length of audio file
    print(len(wav_file))
    # OUTPUT 60000

    '''
    We can change the attributes of file by
    changeed_audio_segment = audio_segment.set_ATTRIBUTENAME(x)
    '''
    wav_file_new = wav_file.set_frame_rate(50)
    print(wav_file_new.frame_rate)

    # Step 2: Convert the AudioSegment to raw data or a specific format
    # Here we use WAV format
    buffer = io.BytesIO()
    wav_file.export(buffer, format="wav")
    buffer.seek(0)  # Reset buffer position to the beginning

    audio_bytes = buffer.read()
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    payload = {
          'type': 'audio',
          'content': audio_base64,
    }

    payload_json = json.dumps(payload)

    await client.send(payload_json)

    response = await client.recv()
    print(f"{response =}")

    client.close()
    # assert response == "pong"