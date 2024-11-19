import base64
import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset


class TTSModule:
    def __init__(self, model_name="microsoft/speecht5_tts"):
        self.model_name = model_name

    def load_model(self):
        self.processor = SpeechT5Processor.from_pretrained(model_name)
        self.model = SpeechT5ForTextToSpeech.from_pretrained(model_name)
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    def synthesize(self, text: str) -> str:
        inputs = self.processor(text, return_tensors="pt")

        # load xvector containing speaker's voice characteristics from a dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

        speech = self.model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

        audio_bytes = speech.numpy().tobytes()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return audio_base64

# Singleton instance for TTS Module
tts_module = TTSModule()