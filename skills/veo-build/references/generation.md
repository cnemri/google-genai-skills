# Veo 3 Video Generation

This guide covers creating videos from scratch using Text-to-Video and Image-to-Video with the Google Gen AI SDK.

## Models

- `veo-3.1-generate-001`: High quality, standard latency.
- `veo-3.1-fast-generate-001`: Lower latency, optimized for speed.

## Text-to-Video

Generate a video purely from a text prompt.

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="YOUR_PROJECT", location="us-central1")

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="a cinematic wide shot of a detective interrogating a rubber duck in a dark room",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",      # "16:9" or "9:16"
        resolution="1080p",       # "720p", "1080p", or "4k" (4k adds latency)
        duration_seconds=6,       # 4, 6, or 8
        number_of_videos=1,       # 1 or 2
        person_generation="allow_adult", # "allow_adult" or "dont_allow"
        enhance_prompt=True,      # Let the model rewrite/improve your prompt
        generate_audio=True,      # Generate synchronized audio
        output_gcs_uri="gs://your-bucket/output.mp4" # Optional: Save directly to GCS
    ),
)
```

## Image-to-Video

Generate a video starting from a static image context. The model animates the image based on the prompt.

```python
operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="zoom out of the flower field, play whimsical music",
    image=types.Image.from_file(location="path/to/image.png"),
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        duration_seconds=6,
        resolution="1080p",
        generate_audio=True,
    ),
)
```

## Prompt Engineering Parameters

When constructing prompts, consider these dimensions for better control:

### Camera Control
- **Angles**: `Eye-Level Shot`, `Low-Angle Shot`, `High-Angle Shot`, `Bird's-Eye View`, `Close-Up`, `Wide Shot`, `Over-the-Shoulder Shot`, `Drone Shot`.
- **Movement**: `Pan (left/right)`, `Tilt (up/down)`, `Zoom (In/Out)`, `Dolly (In/Out)`, `Truck (Left/Right)`, `Handheld`, `Shaky Cam`.

### Visual Style
- **Styles**: `Photorealistic`, `Cinematic`, `Vintage`, `Claymation style`, `Stop-motion animation`, `Film noir style`, `Cyberpunk`.
- **Lighting**: `Golden hour glow`, `Volumetric lighting`, `Film noir style`, `High-key lighting`.

### Audio Hints
- Mention sound effects or dialogue directly in the prompt (e.g., "Sound of waves crashing", "The person says: 'Hello world'").
