# Gemini-prompt r6 Dustly (Claude, 15 nov)
Bijlage: **`r3_a.png`** (alleen die). Nieuw gesprek. Het woord "Gastly" staat niet in de prompt.

## Jordi (letterlijk)
- r3: "kijk beter, alleen ik weet niet of ik fan van de kleuren ben" · "ik vind dat roestbruin niet mooi en idd te massief" · "een wolk of gaswolk is het leukste"
- r5 (`r5_a.png`, zonder bijlage): "het is weer precies gastly"

## Waarom (Claude)
- Ook zonder bijlage en naam tekent Gemini bij "wolk met boos gezicht" Gastly. Alleen r3 week af. r3 als bijlage gebruiken: Gemini kopieert een bijlage (GEMINI.md), en hier is dat wat we willen (vorm en gezicht), met alleen kleur en massiviteit anders.

## Prompt

```
The attached image is my own Pokémon design, "Dustly", a Cosmic/Poison type: a living cloud of gas and dust from space. Redraw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style): 64x64 pixel art, at most 16 colours, light from the top left, plain white background, no ground, no shadow, no glow, no sparkles.

KEEP exactly: the face (the small slanted eyes and the grin with two fangs, left of the centre), the three-quarter view facing left, the overall roughly round cloud silhouette and its size.

CHANGE only two things:
1. COLOUR: replace the rust-brown, orange and pink with dark grey-brown smoke colours: darkest grey-brown around the face, lighter, softer grey-brown on the outer parts. Keep only a THIN rim of rose-pink with a little pale orange along the upper left edge, one or two pixels wide.
2. LESS SOLID: it must read as soft gas, not as a solid lump. Make the lumps softer and less sharply outlined (no dark lines between the lumps inside the cloud), and let the outer edge, especially on the right and bottom, break up into a few loose wisps and small drifting puffs with gaps of white between them.

AVOID: adding a ball or sphere around the face, a dark circle behind the face, making the face bigger, rust-brown, orange or pink lumps, black, purple, a ghost look, arms, hands, legs, stars or sparkles, glow effects, a glossy 3D render.
```
