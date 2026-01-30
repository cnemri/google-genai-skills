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
    parser = argparse.ArgumentParser(description="Edit videos using Veo 2 models.")
    parser.add_argument("--video", required=True, help="URI or Path to input video")
    parser.add_argument("--mask", required=True, help="Path to mask image")
    parser.add_argument("--mode", required=True, choices=["REMOVE", "REMOVE_STATIC", "INSERT"], help="Edit mode")
    parser.add_argument("--prompt", help="Text prompt (required for INSERT mode)")
    parser.add_argument("--model", default="veo-2.0-generate-preview", help="Model to use (default: veo-2.0-generate-preview)")
    parser.add_argument("--output", default="edited_video.mp4", help="Output filename")
    
    args = parser.parse_args()
    
    if args.mode == "INSERT" and not args.prompt:
        print("Error: --prompt is required for INSERT mode.")
        sys.exit(1)
        
    client = get_client()
    
    try:
        # Determine Mask Mode
        mask_mode_map = {
            "REMOVE": types.VideoGenerationMaskMode.REMOVE,
            "REMOVE_STATIC": types.VideoGenerationMaskMode.REMOVE_STATIC,
            "INSERT": types.VideoGenerationMaskMode.INSERT
        }
        
        # Configure Mask
        if not os.path.exists(args.mask):
            print(f"Error: Mask image '{args.mask}' not found.")
            sys.exit(1)
            
        mask = types.VideoGenerationMask(
            image=types.Image.from_file(location=args.mask),
            mask_mode=mask_mode_map[args.mode]
        )
        
        # Configure Source Video
        # Check if local or GCS URI
        video_source = None
        if args.video.startswith("gs://"):
             video_source = types.Video(uri=args.video, mime_type="video/mp4")
        elif os.path.exists(args.video):
             # For local files, we might need to upload or read bytes.
             # The SDK usually expects a URI for videos, or we can try from_file if supported for Video?
             # `types.Video` supports `uri`.
             # Let's assume for editing we prefer GCS URIs, but if local, we try to pass it?
             # Usually `types.Video` takes URI. Uploading might be needed.
             # For now, let's warn if it's local but try to pass path?
             print("Note: Local video files might need to be uploaded to GCS for best performance.")
             # We can't easily upload here without google-cloud-storage lib.
             # We'll try passing the path as uri (some SDKs handle local paths by uploading temporarily).
             # If not, we'll fail.
             video_source = types.Video(uri=args.video, mime_type="video/mp4")
        else:
             print(f"Error: Video '{args.video}' not found.")
             sys.exit(1)

        source_args = {
            "video": video_source
        }
        if args.mode == "INSERT":
            source_args["prompt"] = args.prompt
            
        source = types.GenerateVideosSource(**source_args)

        config = types.GenerateVideosConfig(
            mask=mask,
            enhance_prompt=True
        )

        print(f"Submitting video editing job to {args.model}...")
        operation = client.models.generate_videos(
            model=args.model,
            source=source,
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
        print(f"Error editing video: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
