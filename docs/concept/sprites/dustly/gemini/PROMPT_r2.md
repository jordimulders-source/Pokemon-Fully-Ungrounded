# Gemini-prompt r2 Dustly (Claude, 15 nov)
Bijlage: `../referenties/gastly_gen3_8x.png` (alleen Gastly). **Nieuw gesprek**, r1 niet meesturen (GEMINI.md: vorige versie als bijlage = Gemini kopieert hem).

## Jordi (letterlijk)
- Over r1 (`r1_a.png`): "dit is nog teveel gastly"
- "alleen de ogen en de mond hoeven te blijven"
- Eerder: "ja een wolk, rondachtig zoals gen 1"

## Keuzes Claude (Jordi heeft hier niets over gezegd; schrappen of aanpassen mag)
- Geen bal in de wolk: het hele lijf is één bobbelige donkere stofwolk (voorstel A).
- Geen losse gaswolkjes eromheen (dat is Gastly's aura); het roze zit in de wolk zelf: de rafelrand waar de wolk dun wordt en een belichte rand linksboven (voorstel C, als lichtere pixels, geen gloed).
- Gezicht iets uit het midden (linksboven, driekwart links).

## Prompt

```
Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style): 64x64 pixel art, at most 16 colours, light from the top left, plain white background, no ground, no shadow, no glow, no sparkles, no effects outside the creature.

The Pokémon is "Dustly", a Cosmic/Poison type based on a BOK GLOBULE: a small, dark, dense cloud of dust in space in which a star will later be born. It is NOT a ghost and NOT related to Gastly. ONLY its eyes and mouth are the same as Gastly's; everything else must look different from Gastly.

FACE: the attached sprite is GASTLY. Copy ONLY the eyes and the grin with fangs exactly (same shape, same size), turned into the three-quarter view. Do NOT copy anything else from Gastly: not its round black ball, not its purple gas aura, not its composition.

BODY: there is NO ball inside. The whole body is ONE lumpy, roughly round cloud of dark dust, like a thick dark storm cloud: bumpy, uneven outline made of rounded lumps of different sizes, a few lumps sticking out further than others. The cloud is darkest (almost black, dark brown-black) in the middle and dark reddish-brown towards the edge. Where the cloud thins out at the edge it frays into small ragged clumps.
LIGHT: the top left edge of the cloud is lit by a nearby star: a thin rim of rose-pink and pale orange pixels along the top left lumps, part of the cloud itself, not a glow.
The face sits in the dark cloud, slightly to the upper left.
There are NO separate puffs or blobs of gas floating around the cloud.

POSE: a three-quarter view facing LEFT, floating in space. Compact so it fits in a square; the cloud fills about two thirds of the width of the image, centred.

AVOID: a black ball or sphere inside the cloud, a smooth round outline, a ring or halo of gas around the body, floating pink blobs around it, Gastly's purple, a ghost look, arms, hands, legs, a tail, stars or sparkles, glow effects, a cute plush, chibi or Neopets look, a glossy 3D render.
```
