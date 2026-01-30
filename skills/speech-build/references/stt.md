# Speech-to-Text (STT) - Chirp 3

Chirp 3 offers state-of-the-art multilingual transcription and speaker diarization.

## Transcribe Audio (Synchronous)
For audio < 1 minute.

```python
from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

client = speech_v2.SpeechClient(...)

config = cloud_speech.RecognitionConfig(
    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    model="chirp_3",
    language_codes=["auto"], # Language identification
)

request = cloud_speech.RecognizeRequest(
    recognizer="projects/.../locations/.../recognizers/_",
    config=config,
    content=audio_bytes, # or uri="gs://..."
)

response = client.recognize(request=request)
```

## Batch Recognition
For long audio files.

```python
request = cloud_speech.BatchRecognizeRequest(
    recognizer=recognizer,
    config=config,
    files=[cloud_speech.BatchRecognizeFileMetadata(uri="gs://...")],
    recognition_output_config=cloud_speech.RecognitionOutputConfig(
        gcs_output_config=cloud_speech.GcsOutputConfig(uri="gs://output-bucket")
    ),
)
operation = client.batch_recognize(request=request)
result = operation.result()
```

## Speaker Diarization
Identify different speakers.

```python
config = cloud_speech.RecognitionConfig(
    features=cloud_speech.RecognitionFeatures(
        diarization_config=cloud_speech.SpeakerDiarizationConfig(),
    ),
    model="chirp_3",
    # ...
)
```

## Streaming STT
Real-time transcription.

```python
# Create generator yielding StreamingRecognizeRequest
requests = create_streaming_requests(audio_file)
responses = client.streaming_recognize(requests=requests)
for response in responses:
    print(response.results[0].alternatives[0].transcript)
```
