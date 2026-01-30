# Vertex AI Veo Prompting Guide

This guide provides a comprehensive overview of how to write effective prompts for Veo, Google's text-to-video and image-to-video generation model.

## Core Components

A well-structured prompt typically includes:
1.  **Subject**: The main character, object, or focus.
2.  **Action**: What the subject is doing.
3.  **Scene/Context**: The environment, setting, and background.
4.  **Cinematography**: Camera angles, movements, and lens effects.
5.  **Visual Style**: The overall aesthetic, lighting, and mood.
6.  **Ambiance**: Sensory details.
7.  **Audio**: Sound effects or speech.

## Detailed Options

### Cinematography (Camera & Lens)

**Camera Angles**
- *Eye-Level Shot*: Neutral perspective.
- *Low-Angle Shot*: Subject appears powerful.
- *High-Angle Shot*: Subject appears small/vulnerable.
- *Bird's-Eye View / Top-Down*: Directly from above.
- *Dutch Angle / Canted Angle*: Tilted to convey unease.
- *Close-Up / Extreme Close-Up*: Emphasizes emotions/details.
- *Wide Shot / Establishing Shot*: Shows context.
- *Over-the-Shoulder*: Behind one person looking at another.
- *Point-of-View (POV)*: Character's visual perspective.

**Camera Movements**
- *Static/Fixed*: No movement.
- *Pan (Left/Right)*: Horizontal rotation.
- *Tilt (Up/Down)*: Vertical rotation.
- *Dolly (In/Out)*: Camera moves closer/further.
- *Zoom (In/Out)*: Lens focal length change.
- *Truck (Left/Right)*: Camera moves laterally.
- *Pedestal (Up/Down)*: Camera moves vertically.
- *Crane / Aerial / Drone Shot*: High altitude, sweeping.
- *Handheld / Shaky Cam*: Realism or unease.
- *Whip Pan*: Fast blur pan.

**Lens & Optical Effects**
- *Wide-Angle (e.g., 24mm)*: Broader view, exaggerated perspective.
- *Telephoto (e.g., 85mm)*: Compressed perspective, isolation.
- *Shallow Depth of Field / Bokeh*: Blurred background.
- *Deep Depth of Field*: Everything in focus.
- *Lens Flare*: Bright light source effect.
- *Rack Focus*: Shifting focus between subjects.
- *Vertigo Effect (Dolly Zoom)*: Disorienting distortion.

### Visual Style & Aesthetics
- *Photorealistic / Cinematic*: High fidelity.
- *Vintage / Film Noir*: Sepia, grainy, high contrast black & white.
- *Animation Styles*: 3D cartoon, Claymation, Stop-motion, Anime.
- *Artistic*: Impressionist (Van Gogh), Surrealist.
- *Lighting*: High-key (bright), Low-key (dark/moody), Golden hour, Volumetric (God rays), Backlighting (silhouette).

### Temporal Elements
- *Pacing*: Slow-motion, Fast-paced action.
- *Evolution*: Time-lapse, Hyperlapse.
- *Rhythm*: Pulsating light, Rhythmic movement.

## Best Practices

*   **Be Specific**: Avoid "A man walking." Use "Eye-level medium shot of a young man in a soaked trench coat..."
*   **Negative Prompts**: Define what to exclude (e.g., "Negative prompt: blurry, distorted, text, watermark").
*   **Iterate**: Use Gemini to rewrite prompts for better detail.

## Audio (Preview)
Specify sound effects or speech clearly.
- "The audio features water splashing."
- "The man says, 'Where is the rabbit?'"
