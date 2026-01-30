# Veo 2 Video Editing

This guide covers video editing tasks (inpainting) using the Veo 2 model. These operations require a source video and a mask image.

## Model
- `veo-2.0-generate-preview`

## Concepts
- **Inpainting**: Modifying a specific region of a video defined by a mask.
- **Mask**: An image where white pixels (255) represent the area to edit, and black pixels (0) represent the area to keep.
- **Modes**:
    - `REMOVE`: Dynamic inpainting. Removes an object selected in the first frame mask throughout the video.
    - `REMOVE_STATIC`: Static inpainting. Applies the mask to *every* frame (good for watermarks or fixed camera obstructions).
    - `INSERT`: Adds new content into the masked area based on a prompt.

## Remove Object (Dynamic)

Removes an object identified by the mask in the first frame.

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="YOUR_PROJECT", location="us-central1")

operation = client.models.generate_videos(
    model="veo-2.0-generate-preview",
    source=types.GenerateVideosSource(
        video=types.Video(uri="gs://bucket/source_video.mp4", mime_type="video/mp4")
    ),
    config=types.GenerateVideosConfig(
        mask=types.VideoGenerationMask(
            image=types.Image.from_file(location="mask.png"),
            mask_mode=types.VideoGenerationMaskMode.REMOVE,
        ),
        enhance_prompt=True, # Recommended
    ),
)
```

## Remove Static Object

Removes a static element (like a logo) that is in the same place in every frame.

```python
config=types.GenerateVideosConfig(
    mask=types.VideoGenerationMask(
        image=types.Image.from_file(location="static_mask.png"),
        mask_mode=types.VideoGenerationMaskMode.REMOVE_STATIC,
    ),
    # Optional prompt to guide what replaces the background
    # prompt="a mountain landscape", 
)
```

## Insert Object

Inserts a new object into the masked area defined by the prompt.

```python
operation = client.models.generate_videos(
    model="veo-2.0-generate-preview",
    source=types.GenerateVideosSource(
        prompt="a sheep", # The object to insert
        video=types.Video(uri="gs://bucket/truck.mp4", mime_type="video/mp4")
    ),
    config=types.GenerateVideosConfig(
        mask=types.VideoGenerationMask(
            image=types.Image.from_file(location="mask.png"),
            mask_mode=types.VideoGenerationMaskMode.INSERT,
        ),
        output_gcs_uri="gs://bucket/output_with_sheep.mp4",
        enhance_prompt=True,
    ),
)
```
