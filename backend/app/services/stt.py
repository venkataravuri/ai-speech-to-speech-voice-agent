from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import numpy as np

class STTModule:
    def __init__(self, model_name="openai/whisper-tiny"):
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
    
    def transcribe(self, audio_chunks: bytes) -> str:
        audio_array = np.frombuffer(audio_chunks, dtype=np.float32)
        input_features = self.processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features
        input_features = input_features.to(self.device)
        predicted_ids = self.model.generate(input_features)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription
