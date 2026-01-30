# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
#     "pillow",
# ]
# ///
import os
import argparse
import sys
from google import genai
from google.genai import types
from PIL import Image
import io

def get_client():
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    use_vertex = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower()
    
    if project and location and use_vertex in ("1", "true"):
        return genai.Client(vertexai=True, project=project, location=location)
        
    print("Error: specific environment variables not found.")
    print("Please set GOOGLE_API_KEY or GEMINI_API_KEY.")
    print("OR set GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION and GOOGLE_GENAI_USE_VERTEXAI=1")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate images using Nano Banana models.")
    parser.add_argument("prompt", help="The text prompt for image generation")
    parser.add_argument("--model", default="gemini-3-pro-image-preview", help="Model to use (default: gemini-3-pro-image-preview)")
    parser.add_argument("--output", default="generated_image.png", help="Output filename")
    parser.add_argument("--aspect-ratio", default="1:1", help="Aspect ratio (e.g., 1:1, 16:9, 4:3, 3:4, 9:16)")
    parser.add_argument("--safety-filter-level", default="BLOCK_NONE", help="Safety filter level")
    
    args = parser.parse_args()
    
    client = get_client()
    
    try:
        response = client.models.generate_content(
            model=args.model,
            contents=args.prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=args.aspect_ratio,
                ),
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold=args.safety_filter_level
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold=args.safety_filter_level
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HARASSMENT",
                        threshold=args.safety_filter_level
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HATE_SPEECH",
                        threshold=args.safety_filter_level
                    ),
                ]
            )
        )
        
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    img = Image.open(io.BytesIO(part.inline_data.data))
                    img.save(args.output)
                    print(f"Image saved to {args.output}")
                    return
        print("No image generated.")
            
    except Exception as e:
        print(f"Error generating image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
