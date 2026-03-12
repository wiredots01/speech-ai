import numpy as np
import matplotlib.pyplot as plt

import librosa
import librosa.display
import soundfile as sf
import speech_recognition as sr

from jiwer import wer, cer
from IPython.display import Audio

import whisper

import csv
import os
import tempfile
import wave

from gtts import gTTS


import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


file_path = 'dream.wav'


audio_signal, sample_rate = librosa.load(file_path, sr=None)
print(sample_rate)

# plt.figure(figsize=(12, 4))
# librosa.display.waveshow(audio_signal, sr=sample_rate)
# plt.title('Waveform')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.show()


recognizer = sr.Recognizer()

def transcribe_audio(file_path):
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(text)
        return text    
transcribed_text = transcribe_audio(file_path)
print(transcribed_text)

ground_truth = """A Dream Within a Dream By Edgar Allan Poe Take this kiss upon the brow! And, in parting from you now, Thus much let me avow You are not wrong, who deem That my days have been a dream; Yet if hope has flown away In a night, or in a day, In a vision, or in none, Is it therefore the less gone? All that we see or seem Is but a dream within a dream. I stand amid the roar Of a surf-tormented shore, And I hold within my hand Grains of the golden sand How few! yet how they creep Through my fingers to the deep, While I weep while I weep! O God! can I not grasp Them with a tighter clasp? O God! can I not save One from the pitiless wave? Is all that we see or seem But a dream within a dream?"""

def calculate_error(ground_truth, transcribed_text):
    calculated_wer = wer(ground_truth, transcribed_text)
    calculated_cer = cer(ground_truth, transcribed_text)
    print(f"Word Error Rate (WER): {calculated_wer:.4f}")
    print(f"Character Error Rate (CER): {calculated_cer:.4f}")

# calculated_wer = wer(ground_truth, transcribed_text)
# calculated_cer = cer(ground_truth, transcribed_text)
# print(f"Word Error Rate (WER): {calculated_wer:.4f}")
# print(f"Character Error Rate (CER): {calculated_cer:.4f}")

calculate_error(ground_truth, transcribed_text)
model = whisper.load_model("base")
result = model.transcribe(file_path)
trasncribed_text_whisper = result["text"]

print("***** using whisper ****")
print(result["text"])
print(result["language"])

calculate_error(ground_truth, trasncribed_text_whisper)



text = """This is wiredots testing the text to speech recognition, This is just a test by the way. """
tts = gTTS(text=text, lang='en')

tts.save("./test-output.mp3")

