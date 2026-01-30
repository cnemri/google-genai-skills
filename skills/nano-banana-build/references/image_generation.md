# Image Generation

Gemini 2.5 Flash Image and Gemini 3 Pro Image (Nano Banana) support advanced image generation capabilities.

## Text-to-Image

Generate images from text prompts.

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents="A futuristic cityscape at sunset",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            # image_size="1K" # Optional
        ),
        candidate_count=1,
    ),
)

for part in response.candidates[0].content.parts:
    if part.inline_data:
        # Display or save image
        image = part.as_image()
        image.save("generated.png")
```

## Interleaved Text & Image

Generate tutorials or stories with mixed text and image outputs.

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents="Create a 3-step tutorial for making a sandwich. For each step, provide text and an illustration.",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    ),
)
```

## Image Sizes (Gemini 3 Pro Image)

Gemini 3 Pro Image supports `1K`, `2K`, and `4K`.

```python
config=types.GenerateContentConfig(
    image_config=types.ImageConfig(
        image_size="2K",
        aspect_ratio="1:1"
    )
)
```
