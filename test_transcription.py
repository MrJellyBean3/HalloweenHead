from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
import io

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="transcription_secret.json"

def transcribe_stream(stream_file):
    print("starting")
    """Transcribes audio from a stream."""
    client = speech.SpeechClient()

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()
    
    # In this case, we're reading the file in chunks
    stream = [content]
    
    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)
    
    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    
    streaming_config = types.StreamingRecognitionConfig(config=config)
    
    responses = client.streaming_recognize(streaming_config, requests)
    
    for response in responses:
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

# Replace with the path to your audio file
stream_file_path = "audio_recording.wav"
transcribe_stream(stream_file_path)
