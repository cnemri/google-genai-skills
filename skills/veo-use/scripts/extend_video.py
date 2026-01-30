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
    parser = argparse.ArgumentParser(description="Extend videos using Veo 3 models.")
    parser.add_argument("--video", required=True, help="URI or Path to input video")
    parser.add_argument("--prompt", required=True, help="Description of the extended content")
    parser.add_argument("--duration", type=int, default=6, help="Duration to add in seconds")
    parser.add_argument("--model", default="veo-3.1-generate-preview", help="Model to use (default: veo-3.1-generate-preview)")
    parser.add_argument("--output", default="extended_video.mp4", help="Output filename")
    
    args = parser.parse_args()
    
    client = get_client()
    
    try:
        # Configure Source Video
        video_source = None
        if args.video.startswith("gs://"):
             video_source = types.Video(uri=args.video, mime_type="video/mp4")
        elif os.path.exists(args.video):
             print("Note: Local video files might need to be uploaded to GCS for best performance.")
             video_source = types.Video(uri=args.video, mime_type="video/mp4")
        else:
             print(f"Error: Video '{args.video}' not found.")
             sys.exit(1)

        config = types.GenerateVideosConfig(
            duration_seconds=args.duration,
            generate_audio=True,
        )

        print(f"Submitting video extension job to {args.model}...")
        operation = client.models.generate_videos(
            model=args.model,
            prompt=args.prompt,
            video=video_source,
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
             except Exception as e:
                 print(f"Failed to save video using .save(): {e}")
                 if hasattr(vid, 'video') and hasattr(vid.video, 'uri'):
                     print(f"Video generated at URI: {vid.video.uri}")
                 else:
                     print("Video generated, but could not save locally.")

    except Exception as e:
        print(f"Error extending video: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
