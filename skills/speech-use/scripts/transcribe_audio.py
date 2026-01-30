# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-cloud-speech",
# ]
# ///
import argparse
import os
import sys
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.api_core.client_options import ClientOptions

def get_client(location="us"):
    api_endpoint = f"{location}-speech.googleapis.com" if location != "global" else "speech.googleapis.com"
    client_options = ClientOptions(api_endpoint=api_endpoint)
    return SpeechClient(client_options=client_options)

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using Chirp 3.")
    parser.add_argument("audio_file", help="Path to input audio file")
    parser.add_argument("--model", default="chirp_3", help="Model ID (default: chirp_3)")
    parser.add_argument("--language", default="auto", help="Language code (default: auto)")
    parser.add_argument("--project-id", help="Google Cloud Project ID")
    parser.add_argument("--location", default="us", help="Location (e.g. us, eu, global)")
    parser.add_argument("--output", default="transcript.txt", help="Output text filename")

    args = parser.parse_args()
    
    project_id = args.project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Error: --project-id or GOOGLE_CLOUD_PROJECT env var is required.")
        sys.exit(1)

    client = get_client(args.location)
    
    try:
        with open(args.audio_file, "rb") as f:
            content = f.read()
            
        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            model=args.model,
            language_codes=[args.language],
            features=cloud_speech.RecognitionFeatures(
            #    enable_word_time_offsets=True,
            ),
        )

        request = cloud_speech.RecognizeRequest(
            recognizer=f"projects/{project_id}/locations/{args.location}/recognizers/_",
            config=config,
            content=content,
        )

        print(f"Transcribing {args.audio_file}...")
        response = client.recognize(request=request)
        
        full_transcript = ""
        for result in response.results:
            transcript = result.alternatives[0].transcript
            full_transcript += transcript + "
"
            
        print("Transcript:")
        print(full_transcript)
        
        with open(args.output, "w") as f:
            f.write(full_transcript)
        print(f"Transcript saved to {args.output}")

    except Exception as e:
        print(f"Error transcribing audio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
