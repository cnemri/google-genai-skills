# Model Capabilities & Differences

Choose the model best suited for your specific use case.

| Feature | Gemini 2.5 Flash Image (Nano Banana) | Gemini 3 Pro Image Preview (Nano Banana Pro) |
| :--- | :--- | :--- |
| **Optimization** | Speed, efficiency, high-volume tasks. | Professional asset production, complex reasoning. |
| **Max Resolution** | 1024x1024 (1K) | Up to 4096x4096 (4K) |
| **Thinking Process** | No | Default "Thinking" process to refine composition. |
| **Grounding** | No | Google Search Grounding supported. |
| **Reference Images** | Best with up to 3 images. | Supports up to 14 images (5 humans, 6 objects). |
| **Text Rendering** | Good | Advanced, high-fidelity text rendering. |

## Aspect Ratios & Resolutions

### Gemini 2.5 Flash Image

| Aspect Ratio | Resolution | Tokens |
| :--- | :--- | :--- |
| 1:1 | 1024x1024 | 1290 |
| 9:16 | 768x1344 | 1290 |
| 16:9 | 1344x768 | 1290 |
| 4:3 | 1184x864 | 1290 |
| 3:4 | 864x1184 | 1290 |

### Gemini 3 Pro Image Preview

Supports `1K`, `2K`, and `4K` sizes. Use uppercase 'K' (e.g., `2K`).

| Aspect Ratio | 1K Res | 1K Tokens | 2K Res | 2K Tokens | 4K Res | 4K Tokens |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1:1 | 1024x1024 | 1120 | 2048x2048 | 1120 | 4096x4096 | 2000 |
| 9:16 | 768x1376 | 1120 | 1536x2752 | 1120 | 3072x5504 | 2000 |
| 16:9 | 1376x768 | 1120 | 2752x1536 | 1120 | 5504x3072 | 2000 |
| 4:3 | 1200x896 | 1120 | 2400x1792 | 1120 | 4800x3584 | 2000 |
| 3:4 | 896x1200 | 1120 | 1792x2400 | 1120 | 3584x4800 | 2000 |

## Configuration Example

```python
config = types.GenerateContentConfig(
    image_config=types.ImageConfig(
        aspect_ratio="16:9",
        image_size="2K", # Only for Gemini 3 Pro
    )
)
```
