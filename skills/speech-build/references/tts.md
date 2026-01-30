# Text-to-Speech (TTS)

## Overview
Google Cloud and Vertex AI offer multiple TTS solutions:
1.  **Gemini-TTS:** Advanced, controllable speech generation using Gemini 2.5 models.
2.  **Chirp 3 HD:** High-fidelity, natural-sounding voices.
3.  **Instant Custom Voice (Chirp 3):** Create custom voices from short audio samples (allowlist required).

## Gemini-TTS (Preview)
Use `gemini-2.5-flash-preview-tts` for controllable speech.

### Single Speaker
```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="Say cheerfully: Have a wonderful day!",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
            )
        ),
    )
)
# Save response.candidates[0].content.parts[0].inline_data.data to .wav
```

### Multi-Speaker
```python
config = types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
            speaker_voice_configs=[
                types.SpeakerVoiceConfig(
                    speaker='Joe',
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
                    )
                ),
                types.SpeakerVoiceConfig(
                    speaker='Jane',
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Puck')
                    )
                ),
            ]
        )
    )
)
```

## Chirp 3 HD (Vertex AI)
High-fidelity voices for general use.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-tts", # or chirp-3-hd via speech client
    contents="Hello world",
    config=types.GenerateContentConfig(
        speech_config=types.SpeechConfig(
            language_code="en-US",
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Aoede")
            )
        )
    )
)
```

## Instant Custom Voice (Chirp 3)
*Requires Allowlist.* Uses `voices:generateVoiceCloningKey`.

1.  **Create Key:** Post reference & consent audio to `generateVoiceCloningKey`.
2.  **Synthesize:** Use the key in `voice_clone` config.

```python
# Synthesis with key
request_body = {
    "input": {"text": "Hello form my custom voice"},
    "voice": {
        "language_code": "en-US",
        "voice_clone": {"voice_cloning_key": "YOUR_KEY"}
    },
    "audioConfig": {"audioEncoding": "LINEAR16"}
}
```
