# Prompting for Gemini-TTS

Gemini-TTS understands natural language instructions for **how** to speak.

## Structure
1.  **Audio Profile:** Persona/Archetype (e.g., "Radio DJ").
2.  **Scene:** Environment/Vibe (e.g., "Late night studio").
3.  **Director's Notes:** Specifics on Style, Pacing, Accent.
4.  **Transcript:** The actual text to read.

## Examples

### Single Speaker
```
Say in a spooky whisper:
"By the pricking of my thumbs... Something wicked this way comes"
```

### Multi-Speaker
```
Make Speaker1 sound tired and bored, and Speaker2 sound excited and happy:

Speaker1: So... what's on the agenda today?
Speaker2: You're never going to guess!
```

### Advanced Prompt
```
# AUDIO PROFILE: Jaz R. (Radio DJ)
## THE SCENE: The London Studio
It is 10:00 PM... upbeat atmosphere.

### DIRECTOR'S NOTES
Style: The "Vocal Smile". Bright, sunny.
Pace: Fast, bouncing cadence. No dead air.
Accent: Estuary accent from Brixton, London.

#### TRANSCRIPT
Yes, massive vibes in the studio! ...
```
