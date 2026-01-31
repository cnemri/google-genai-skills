# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "google-auth",
# ]
# ///
import argparse
import base64
import json
import os
import sys
import requests
import google.auth
import google.auth.transport.requests

def get_credentials():
    credentials, _ = google.auth.default()
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials

def wav_to_base64(file_path):
    try:
        with open(file_path, "rb") as wav_file:
            encoded_string = base64.b64encode(wav_file.read()).decode("utf-8")
            return encoded_string
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def create_instant_custom_voice_key(reference_audio_path, consent_audio_path, project_id, location="us"):
    
    api_endpoint = "texttospeech.googleapis.com"
    if location != "global" and location != "us":
         # Regional endpoints might differ, but instant custom voice is often US/Global.
         # The notebook uses global or us-texttospeech. 
         # Let's default to texttospeech.googleapis.com as per notebook example for global/us.
         pass

    url = f"https://{api_endpoint}/v1beta1/voices:generateVoiceCloningKey"

    reference_audio_b64 = wav_to_base64(reference_audio_path)
    consent_audio_b64 = wav_to_base64(consent_audio_path)

    request_body = {
        "reference_audio": {
            "audio_config": {"audio_encoding": "LINEAR16", "sample_rate_hertz": 24000},
            "content": reference_audio_b64,
        },
        "voice_talent_consent": {
            "audio_config": {"audio_encoding": "LINEAR16", "sample_rate_hertz": 24000},
            "content": consent_audio_b64,
        },
        "consent_script": "I am the owner of this voice and I consent to Google using this voice to create a synthetic voice model.",
        "language_code": "en-US",
    }

    credentials = get_credentials()
    
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "x-goog-user-project": project_id,
        "Content-Type": "application/json; charset=utf-8",
    }

    try:
        response = requests.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("voiceCloningKey")
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        if response is not None:
            print("Response text:", response.text)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Create an Instant Custom Voice key.")
    parser.add_argument("--reference-audio", required=True, help="Path to reference audio file (WAV).")
    parser.add_argument("--consent-audio", required=True, help="Path to consent audio file (WAV).")
    parser.add_argument("--project-id", help="Google Cloud Project ID.")
    
    args = parser.parse_args()
    
    project_id = args.project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Error: --project-id or GOOGLE_CLOUD_PROJECT env var is required.")
        sys.exit(1)

    print("Generating Voice Cloning Key...")
    key = create_instant_custom_voice_key(args.reference_audio, args.consent_audio, project_id)
    
    if key:
        print("SUCCESS! Voice Cloning Key:")
        print(key)
        print("\nSave this key to use with generate_speech.py --voice-cloning-key")
    else:
        print("Failed to generate key.")

if __name__ == "__main__":
    main()
