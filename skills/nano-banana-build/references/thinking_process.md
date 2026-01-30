# Thinking Process & Thought Signatures

Gemini 3 Pro Image Preview uses a default "Thinking" process to refine composition and logic before generation.

## Accessing Thoughts

You can inspect the thoughts that led to the final image.

```python
for part in response.parts:
    if part.thought:
        if part.text:
            print(f"Thought: {part.text}")
        elif part.inline_data:
            # Interim thought image
            image = part.as_image()
            image.show()
```

## Thought Signatures

**Crucial for Multi-turn:** Thought signatures preserve reasoning context across turns.

- **Automatic Handling:** If using `client.chats` or appending the full response object to history, the SDK handles this automatically.
- **Manual Handling:** If manually constructing JSON payloads, you **must** pass back the `thought_signature` field exactly as received.

### Structure
- The first non-thought text part has a signature.
- All inline image parts (except thought images) have signatures.
- Thought parts do **not** have signatures.

Failure to circulate thought signatures may cause the response to fail.
