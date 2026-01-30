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
import time
from google import genai
from google.genai import types

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
    parser = argparse.ArgumentParser(description="Generate videos from image using Veo 3.")
    parser.add_argument("prompt", help="The text prompt for video generation")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--model", default="veo-3.1-generate-001", help="Model to use (default: veo-3.1-generate-001)")
    parser.add_argument("--output", default="generated_video.mp4", help="Output filename")
    parser.add_argument("--aspect-ratio", default="16:9", help="Aspect ratio (16:9 or 9:16)")
    parser.add_argument("--resolution", default="1080p", help="Resolution (720p, 1080p, 4k)")
    parser.add_argument("--duration", type=int, default=6, help="Duration in seconds (4, 6, 8)")
    
    args = parser.parse_args()
    
    client = get_client()
    
    try:
        if not os.path.exists(args.image):
            print(f"Error: Input image '{args.image}' not found.")
            sys.exit(1)

        config = types.GenerateVideosConfig(
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            duration_seconds=args.duration,
            generate_audio=True,
            person_generation="allow_adult",
        )

        print(f"Submitting Image-to-Video job to {args.model}...")
        operation = client.models.generate_videos(
            model=args.model,
            prompt=args.prompt,
            image=types.Image.from_file(location=args.image),
            config=config
        )
        
        print(f"Operation name: {operation.name}")
        
        print("Waiting for operation to complete...")
        while True:
            op_status = client.operations.get(operation)
            if op_status.done:
                break
            time.sleep(10)
            print(".", end="", flush=True)
        
        print("")
        print("Operation complete.")
        
        if op_status.error:
            print(f"Operation failed with error: {op_status.error}")
            sys.exit(1)

        result = op_status.result
        
        if result and result.generated_videos:
             vid = result.generated_videos[0]
             try:
                 if hasattr(vid, 'video'):
                     vid.video.save(args.output)
                     print(f"Video saved to {args.output}")
                 else:
                     print("Error: GeneratedVideo object has no 'video' attribute.")
             except Exception as save_err:
                 print(f"Failed to save video using .save(): {save_err}")
                 if hasattr(vid, 'video') and hasattr(vid.video, 'uri'):
                     print(f"Video generated at URI: {vid.video.uri}")
                 else:
                     print("Video generated, but could not save locally.")
        else:
             print("No video generated in result.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error generating video: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
