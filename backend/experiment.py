import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import librosa
import pydub
import io
import numpy as np
from pydub import AudioSegment

# Load the Whisper model and processor
model_name = "openai/whisper-tiny"
model = WhisperForConditionalGeneration.from_pretrained(model_name)
processor = WhisperProcessor.from_pretrained(model_name)

# Load the audio file
audio_file = "data/you-got-it-1.wav"
audio, sr = librosa.load(audio_file, sr=16000)

print(type(audio))
print(len(audio))

# Set the language to English
language = "en"

audio_segment = AudioSegment.from_wav(audio_file)

# convert to expected format
if audio_segment.frame_rate != 16000: # 16 kHz
    audio_segment = audio_segment.set_frame_rate(16000)
if audio_segment.sample_width != 2:   # int16
    audio_segment = audio_segment.set_sample_width(2)
if audio_segment.channels != 1:       # mono
    audio_segment = audio_segment.set_channels(1)       

print(type(audio_segment.get_array_of_samples())) 
print(len(audio_segment.get_array_of_samples())) 
arr = np.array(audio_segment.get_array_of_samples())
arr = arr.astype(np.float32)/32768.0

# Preprocess the audio
input_values = processor(arr, return_tensors="pt", sampling_rate=sr)
print(f"{input_values["input_features"].shape}")

# Create attention mask
attention_mask = torch.ones_like(input_values["input_features"])

# Generate text
with torch.no_grad():
    predicted_ids = model.generate(input_values["input_features"], attention_mask=attention_mask, language=language)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True, language=language)[0]
    print(f"Transcription: {transcription}")

