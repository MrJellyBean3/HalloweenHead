import os
import io
import multiprocessing
from pvrecorder import PvRecorder
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
import time

from queue import Empty

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="transcription_secret.json"

def transcribe_stream(queue):
    client = speech.SpeechClient()

    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )

    streaming_config = types.StreamingRecognitionConfig(config=config)

    print("transcribing")

    while True:
        try:
            # Attempt to get audio_chunk from queue
            audio_chunk = queue.get(timeout=1)  # timeout in seconds
        except Empty:
            # Handle empty queue situation if necessary
            # You might want to continue or break depending on your use case
            pass
        if audio_chunk is None:
            break

        requests = (types.StreamingRecognizeRequest(audio_content=audio_chunk))
        responses = client.streaming_recognize(streaming_config, [requests])

        for response in responses:
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))

import wave
from io import BytesIO
import struct

def record_audio(queue):
    recorder = PvRecorder(device_index=0, frame_length=512)
    recorder.start()
    t_start = time.time()
    audio = []
    try:
        print("Starting Recording")
        while (time.time() < (t_start + 10)):
            pcm = recorder.read()
            audio.extend(pcm)  # Assuming pcm is a list of integers

            # You might want to send smaller chunks of audio for more real-time transcription
            if len(audio) >= 4096: 
                # Convert list of PCM data to bytes
                byte_data = struct.pack("<" + "h" * len(audio), *audio)
                queue.put(byte_data)
                audio = []  # Clear the audio data
            print(len(audio), end='\r')
    finally:
        recorder.delete()



if __name__ == '__main__':
    queue = multiprocessing.Queue()

    transcriber_process = multiprocessing.Process(target=transcribe_stream, args=(queue,))
    recorder_process = multiprocessing.Process(target=record_audio, args=(queue,))

    transcriber_process.start()
    recorder_process.start()

    transcriber_process.join()
    recorder_process.join()
