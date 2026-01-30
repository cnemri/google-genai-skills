# Image Editing

Nano Banana models support advanced image-to-image capabilities.

## Subject Customization

Change the style or attributes of a subject while preserving its identity.

```python
with open("dog.jpg", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        "Create a pencil sketch of this dog wearing a cowboy hat."
    ],
    config=types.GenerateContentConfig(response_modalities=["IMAGE"])
)
```

## Style Transfer

Apply the style of one image to the content of another.

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents=[
        types.Part.from_uri(file_uri="gs://.../style_ref.png", mime_type="image/png"),
        "Using the concepts and colors from this image, generate a kitchen with the same aesthetic."
    ],
    config=types.GenerateContentConfig(response_modalities=["IMAGE"])
)
```

## Multi-turn Editing (Chat)

Iteratively refine an image in a chat session.

```python
chat = client.chats.create(
    model='gemini-2.5-flash-image',
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)

# First turn
response = chat.send_message("Create an image of a perfume bottle.")
image_data = response.candidates[0].content.parts[1].inline_data.data

# Second turn (pass previous image back)
response = chat.send_message([
    types.Part.from_bytes(data=image_data, mime_type="image/png"),
    "Make the bottle purple."
])
```

## Multiple Reference Images

Combine elements from multiple images.

```python
response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents=[
        types.Part.from_uri(file_uri="gs://.../person.jpg", mime_type="image/jpeg"),
        types.Part.from_uri(file_uri="gs://.../background.png", mime_type="image/png"),
        "Generate an image of the person from the first image standing in the background from the second image."
    ]
)
```
