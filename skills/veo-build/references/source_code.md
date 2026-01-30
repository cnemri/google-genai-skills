# Google GenAI SDK Source Code (Veo)

Use `web_fetch` to retrieve raw code for deep inspection of SDK internals, especially for video generation parameters.

**Base URL:** `https://raw.githubusercontent.com/googleapis/python-genai/main/google/genai/`

## Key Modules for Veo

### Models (Generation Logic)
- **File:** `models.py`
- **URL:** `https://raw.githubusercontent.com/googleapis/python-genai/main/google/genai/models.py`
- **Purpose:** Contains `generate_videos` and `generate_images` methods. Check this for parameter handling.

### Types (Configuration)
- **File:** `types.py`
- **URL:** `https://raw.githubusercontent.com/googleapis/python-genai/main/google/genai/types.py`
- **Purpose:** Definitions for `GenerateVideosConfig`, `PersonGeneration`, `VideoCompressionQuality`, etc.

### Operations (Async Handling)
- **File:** `operations.py`
- **URL:** `https://raw.githubusercontent.com/googleapis/python-genai/main/google/genai/operations.py`
- **Purpose:** Handling LROs (Long Running Operations) returned by video generation.

### Client
- **File:** `client.py`
- **URL:** `https://raw.githubusercontent.com/googleapis/python-genai/main/google/genai/client.py`
