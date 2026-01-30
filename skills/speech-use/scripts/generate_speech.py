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
    parser = argparse.ArgumentParser(description="Generate speech using Gemini-TTS.")
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("--voice", default="Puck", help="Prebuilt voice name (e.g. Kore, Puck). Ignored if --voice-cloning-key is set.")
    parser.add_argument("--voice-cloning-key", help="Instant Custom Voice Cloning Key")
    parser.add_argument("--model", default="gemini-2.5-flash-preview-tts", help="TTS Model")
    parser.add_argument("--output", default="output.wav", help="Output filename")
    
    args = parser.parse_args()
    client = get_client()
    
    try:
        if args.voice_cloning_key:
            print(f"Using Custom Voice Key: {args.voice_cloning_key[:8]}...")
            voice_config = types.VoiceConfig(
                voice_clone=types.VoiceClone(voice_cloning_key=args.voice_cloning_key)
            )
        else:
            print(f"Using Prebuilt Voice: {args.voice}")
            voice_config = types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=args.voice)
            )

        config = types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=voice_config
            )
        )

        print(f"Generating speech with model {args.model}...")
        response = client.models.generate_content(
            model=args.model,
            contents=args.text,
            config=config
        )
        
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if part.inline_data:
                with open(args.output, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"Audio saved to {args.output}")
            else:
                print("No inline audio data found.")
        else:
            print("No candidates returned.")

    except Exception as e:
        print(f"Error generating speech: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
