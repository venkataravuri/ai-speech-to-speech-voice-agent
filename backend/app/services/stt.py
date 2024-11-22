from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import numpy as np
from ..core.logging import logger

class STTModule:
    def __init__(self, model_name="openai/whisper-tiny"):
        self.model_name = model_name

    def load_model(self):
        self.processor = WhisperProcessor.from_pretrained(self.model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(self.model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
    
    def transcribe(self, audio_chunks: bytes) -> str:
        audio_array = np.frombuffer(audio_chunks, dtype=np.float32)
        print(f"{len(audio_array) = }")
        input_features = self.processor(audio_array, return_tensors="pt").input_features
        input_features = input_features.to(self.device)
        predicted_ids = self.model.generate(input_features)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        print(f"Transcription: {transcription}")
        return transcription

# Singleton instance of the STT Module
stt_module = STTModule()