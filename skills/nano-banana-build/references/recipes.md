# Nano Banana Recipes

Practical examples for common tasks using Gemini 2.5 Flash Image and Gemini 3 Pro Image.

## Blank Canvas (Aspect Ratio Control)
Force a specific aspect ratio by providing a blank image.

```python
from PIL import Image
import io

def create_canvas(width=1280, height=720):
    img = Image.new("RGB", (width, height), "white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png")

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        create_canvas(1280, 720),
        "A cinematic wide shot of a desert planet."
    ]
)
```

## Virtual Try-On
Place a garment on a model.

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        types.Part.from_uri(file_uri="gs://.../model.jpg", mime_type="image/jpeg"),
        types.Part.from_uri(file_uri="gs://.../dress.jpg", mime_type="image/jpeg"),
        "Realistically place the dress from the second image onto the person in the first image."
    ]
)
```

## Product Recontextualization
Place a product in a new scene.

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        types.Part.from_uri(file_uri="gs://.../product.png", mime_type="image/png"),
        "Place this product on a marble countertop in a luxury kitchen."
    ]
)
```

## Character Consistency
Maintain a character across different scenes.

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        types.Part.from_uri(file_uri="gs://.../character_ref.png", mime_type="image/png"),
        "Generate an image of this character eating an apple in a park."
    ]
)
```

## Stylized Stickers
Create stickers with transparent backgrounds.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat. It's munching on a green bamboo leaf. The design features bold, clean outlines, simple cel-shading, and a vibrant color palette. The background must be white.",
)
```

## Logo Design
Create modern, minimalist logos using accurate text rendering (Gemini 3 Pro).

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'. The text should be in a clean, bold, sans-serif font. The color scheme is black and white. Put the logo in a circle. Use a coffee bean in a clever way.",
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(aspect_ratio="1:1")
    )
)
```

## Product Mockups
Generate high-resolution commercial photography.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A high-resolution, studio-lit product photograph of a minimalist ceramic coffee mug in matte black, presented on a polished concrete surface. The lighting is a three-point softbox setup designed to create soft, diffused highlights and eliminate harsh shadows. The camera angle is a slightly elevated 45-degree shot to showcase its clean lines. Ultra-realistic, with sharp focus on the steam rising from the coffee. Square image.",
)
```

## Minimalist Backgrounds
Create negative space designs for text overlays.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A minimalist composition featuring a single, delicate red maple leaf positioned in the bottom-right of the frame. The background is a vast, empty off-white canvas, creating significant negative space for text. Soft, diffused lighting from the top left. Square image.",
)
```

## Sequential Art (Comics)
Create storytelling panels using character references.

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Make a 3 panel comic in a gritty, noir art style with high-contrast black and white inks. Put the character in a humorous scene.",
        types.Part.from_uri(file_uri="gs://.../character.jpg", mime_type="image/jpeg")
    ],
)
```

## Grounding with Google Search
Generate images based on real-time data.

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Make a simple but stylish graphic of last night's Arsenal game in the Champion's League",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        image_config=types.ImageConfig(aspect_ratio="16:9")
    )
)
```

## Sketch to Life
Turn a rough drawing into a polished image.

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        types.Part.from_uri(file_uri="gs://.../car_sketch.png", mime_type="image/png"),
        "Turn this rough pencil sketch of a futuristic car into a polished photo of the finished concept car in a showroom. Keep the sleek lines and low profile from the sketch but add metallic blue paint and neon rim lighting."
    ],
)
```

## Multi-Image Composition (Advanced)
Combine up to 14 reference images (Gemini 3 Pro).

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "An office group photo of these people, they are making funny faces.",
        types.Part.from_uri(file_uri="gs://.../person1.png", mime_type="image/png"),
        types.Part.from_uri(file_uri="gs://.../person2.png", mime_type="image/png"),
        types.Part.from_uri(file_uri="gs://.../person3.png", mime_type="image/png"),
        # ... up to 14 images total
    ],
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(aspect_ratio="5:4", image_size="2K")
    )
)
```