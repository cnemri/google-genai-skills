# Veo 3 Advanced Controls

This guide covers advanced generation techniques: Frame Interpolation, Video Extension, and using Asset Reference Images.

## Frame Interpolation

Generates video content that bridges a `first_frame` and a `last_frame`. Useful for creating transitions or animating between two states.

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="YOUR_PROJECT", location="us-central1")

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="a hand reaches in and places a glass of milk", # Optional guidance
    image=types.Image.from_file(location="cookies.png"), # First frame
    config=types.GenerateVideosConfig(
        last_frame=types.Image.from_file(location="cookies-milk.png"), # Last frame
        duration_seconds=8, # Duration of the generated bridge
        aspect_ratio="16:9",
        generate_audio=True,
    ),
)
```

## Video Extension

Extends an existing video clip in time. Requires `veo-3.1-generate-preview`.

```python
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="a butterfly flies in and lands on the flower", # Describes the *new* content
    video=types.Video(uri="gs://bucket/short_clip.mp4", mime_type="video/mp4"),
    config=types.GenerateVideosConfig(
        duration_seconds=7, # How many seconds to ADD to the video
        output_gcs_uri="gs://bucket/extended_clip.mp4",
        generate_audio=True,
    ),
)
```

## Reference-to-Video (Asset Images)

Use up to 3 specific reference images ("assets") to guide the generation. This helps preserve the identity of subjects, objects, or scenes across the video.

### Asset Types
- **Subject**: A person or character.
- **Object**: A product or item.
- **Scene**: A background or environment.

### Code Example

```python
# Load images from GCS or local files
ref_image_1 = types.VideoGenerationReferenceImage(
    image=types.Image.from_file(location="man.png"),
    reference_type="asset",
)
ref_image_2 = types.VideoGenerationReferenceImage(
    image=types.Image.from_file(location="woman.png"),
    reference_type="asset",
)

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview", # or veo-3.1-fast-generate-preview
    prompt="a woman and a man drinking a cup of coffee in a cafe",
    config=types.GenerateVideosConfig(
        reference_images=[ref_image_1, ref_image_2], # List of up to 3 references
        aspect_ratio="16:9",
        duration_seconds=8,
        person_generation="allow_adult",
        generate_audio=True,
    ),
)
```
