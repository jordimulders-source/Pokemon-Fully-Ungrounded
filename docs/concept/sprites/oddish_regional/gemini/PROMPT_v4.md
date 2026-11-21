# Gemini-prompt v4, 20 nov
Bijlage 1: `r2/gemini_v2.png` (vorm kroon, lijf, gezicht). Bijlage 2: `r3/gemini_v3.png` (draadtextuur). Nieuw gesprek.
Jordi: "ja maak die prompt maar, wilde al vragen hoe we ervoor kunnen zorgen dat die goed naar een sprite vertaalt".

```
Attached are two drafts of the same regional form of Oddish (official Gen 3 front sprite style). Combine them into one official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art) that works at real 64x64 size.

FROM IMAGE 1 (keep exactly)
- The white/cream body, the two feet, the walking pose (three-quarter view facing left), the tiny red dot eyes and the small open red mouth.
- The crown: the same number of separate shapes, with the same size, outline shape and placement as the leaves in image 1. Each shape stays a clearly separate, pointed tuft, so the silhouette reads as Oddish.

FROM IMAGE 2
- The material: each tuft is not a leaf but a giant tube worm (Riftia) plume made of red filaments. Show this the way Gen 3 sprites draw hair or feathers: each tuft is one solid clump with a few filament lines inside, and only its tip splits into 2 to 4 short frayed points. No single 1-pixel strands sticking out, no leaf vein.

SPRITE RULES
- Every tuft has its own dark outline (dark red, not black), and the tufts are separated from each other by that outline.
- Red in 4 tones (highlight, light, mid, shadow), light from top left; the back tufts are a bit darker than the front ones.
- 64x64 canvas, max 16 colors in total, 1 px outline around the whole creature, flat Gen 3 shading, no dithering, no anti-aliasing.
- Plain white background. No ground, water, bubbles, shadow or extra effects. One single creature.

AVOID
- No leaves, no green, no flower, no anemone tentacles, no hair mop, no fire or smoke.
```
