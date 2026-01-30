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
    parser = argparse.ArgumentParser(description="Compose images using Nano Banana models.")
    parser.add_argument("--image", action='append', required=True, help="Path to input image(s). Can be used multiple times.")
    parser.add_argument("prompt", help="Instruction for composing the image")
    parser.add_argument("--model", default="gemini-3-pro-image-preview", help="Model to use (default: gemini-3-pro-image-preview)")
    parser.add_argument("--output", default="composed_image.png", help="Output filename")
    parser.add_argument("--aspect-ratio", default="1:1", help="Aspect ratio (e.g., 1:1, 16:9)")
    parser.add_argument("--safety-filter-level", default="BLOCK_NONE", help="Safety filter level")

    args = parser.parse_args()
    
    client = get_client()
    
    try:
        contents = []
        for img_path in args.image:
            if not os.path.exists(img_path):
                print(f"Error: Input image '{img_path}' not found.")
                sys.exit(1)
                
            with open(img_path, "rb") as f:
                image_bytes = f.read()
            
            # Determine mime type roughly
            mime_type = "image/jpeg"
            if img_path.lower().endswith(".png"):
                mime_type = "image/png"
            elif img_path.lower().endswith(".webp"):
                mime_type = "image/webp"
                
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
            
        contents.append(args.prompt)

        response = client.models.generate_content(
            model=args.model,
            contents=contents,
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
        print(f"Error composing image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
