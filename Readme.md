












## Prompts


I'm building to a speech-to-speech AI voice assisant. I already have skeleton code for frontend using ReactJS and backend using FastAPI. I building this application on Windows that does not have GPU. Hence larged ML models usage is not an option.

Now, help me to write code that builds below pipeline with langchain and huggigface libraries,

1. Convert voice audio byte chunks into text (STT) using Whisper tiny model. The model should be loaded once during boot up and used across multiple times for inference. Add text to the context or memory to use as context in future prompts.
2. Wait till user question is complete, not sure how this can be recognized.
3. Once user asked question then, enitre text along with history should be used to prompt Llama 3.2 1b model to get a textual response to user query.
4. Convert text response into voice or speech using a light-weight TTS model. Ths generated voice bytes has to be encoded into base64 and streamed back to frontend using websockets

Give me a modularized code for the above stated requirement.