# Ruimtestation (fase 3), Gemini-prompt r7 – NIEUW gesprek, geen bijlage
r6 (`r6.png`), Jordi: "de panelen kloppen niet".
Lezing Claude (voor te leggen): in r6 staan de panelen alle kanten op (één rechtop door het knooppunt, verschillende hoeken, overlappen elkaar en de modules). Jordi erbij: "linkeroog zit ook niet goed, rechts wel, maar rechts zou gespiegeld kunnen worden" → zijbollen in de prompt als spiegelbeeld (rechts = goed); kan anders in het model door de rechterbol te spiegelen. Basis = prompt r6, alleen het panelenblok vervangen: 3 gespiegelde paren aan de lange arm, alle zes in één vlak en parallel, niets overlapt.

```
Design a Pokémon: an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64×64 pixels, max 16 colors, clean dark outline, plain white background, no ground, no shadow, no effects or glow.

WHAT IT IS: a big living space station, the final evolution of a small one-eyed satellite. It is a pure machine with its own personality, the way Magneton, Metagross and Porygon are Pokémon: no animal parts, no arms, no legs, no mouth.

SIZE AND COMPLEXITY (most important): this is a LARGE, heavy, final-stage Pokémon, clearly more complex than a single satellite or a straight line of modules. It fills the WHOLE 64×64 frame from edge to edge. Each eye-sphere is only a small part of the whole creature.

POSE AND ANGLE: Gen 3 front-sprite 3/4 view facing the viewer's LEFT, seen slightly from above. Everything in this one perspective. Compact in a square.

BUILD (a cross-shaped station): in the middle is a round white node sphere. From it, white cylinder modules branch out in FOUR directions like a cross: a long main arm toward the front-left, a long arm toward the back-right, and two shorter side arms. The modules have different sizes (some wide and short, some long and slim) and each has one or two dark purple bands around it. All joints are purple ring-shaped docking collars. Nothing floats loose: it is one solid connected machine.
FOUR EYE-SPHERES: at the end of EACH of the four arms sits a round white sphere of the same size, each with one eye pointing outward along its arm, like four satellites joined into one station. So we see the eye of the front-left sphere from the front, the two side spheres are exact mirror images of each other: each side eye points straight outward along its own arm (the left one to the left, the right one to the right) and is seen at the same angle, half turned toward the viewer, and the back-right sphere only from behind (its eye is hidden). Each eye is SIMPLE so it reads at small size, but always with a turquoise iris and a dark pupil: one purple ring, a turquoise iris and a dark pupil, flat colors, no extra rings, no shine.
NO ANTENNAE anywhere.

SOLAR PANELS (follow exactly): exactly SIX flat rectangular solar panels in THREE mirrored PAIRS. All six panels lie in ONE flat plane (the horizontal plane of the station, seen from slightly above) and are all parallel to each other, so they all show the same 3/4 perspective and the same tilt. Each pair is attached to the long front-to-back arm: one panel sticks out to the left of the arm and its twin sticks out to the right, both on a short purple rod, like the wings of a real satellite. The pairs sit near the front, at the middle and near the back of the long arm. No panel crosses a module, another panel or an eye-sphere; no panel stands upright; no panel floats loose. Dark navy-purple with a lighter purple grid of only a few large cells (about 2 by 3). Long, but each panel still clearly wide (never thin strips).

DETAIL LEVEL: it must translate well to a 64×64 sprite: big readable shapes, thick parts, medium detail, no thin parts (every part at least a few pixels wide). No rivets, no text, no logos, no flags, no tiny windows, dishes or greebles.

COLORS: pearly white with lavender shading, purple accents (collars, bands, rods, eye rings), dark navy-purple solar panels with lighter purple grid lines, turquoise iris as the only accent. Light from the upper left. Nothing else.

DO NOT: panels in different directions or angles, upright panels, panels overlapping each other, antennae, more or fewer than four eye-spheres, eyes with many rings, a single satellite with two panels, one straight line of modules, a small creature with empty space around it, a ring or wheel, thin orbit lines, starfield or galaxy patterns, stars or Earth around it, a space shuttle, a flat front view or side view, realistic NASA/ISS hardware, a robot with a face screen, arms or legs, cute plush/Neopets style.
```
