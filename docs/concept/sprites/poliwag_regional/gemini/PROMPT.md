# Gemini-prompt: regionale Poliwag, startprompt v1 (25 nov)

Regels: `docs/lessen/GEMINI.md`. Bijlage: `bijlage_poliwag.png` (Poliwags Gen 3-sprite, 8×; alleen voor de herkenbaarheid). Besluiten: `../SPEC.md`.

```
Design a regional form of the Pokémon POLIWAG and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS THE NORMAL POLIWAG. Keep it clearly recognizable as Poliwag: round tadpole body, big eyes, small mouth, the tail and the two little feet, and the spiral on the belly.

CONCEPT
- Type Ice/Poison. A tadpole from cold high mountain ponds in the Andes.
- Based on the harlequin toad (Atelopus), a small, very poisonous toad with bright warning colors.

DESIGN
- Main colors: the bright warning colors of a harlequin toad. Not blue like the normal Poliwag.
- Only a little crystal: a few small pieces of clear ice with red cinnabar inside, growing out of the skin. The animal comes first, the crystal second.
- The belly spiral is a window: the belly is clear ice, and through it you see the poisonous warning colors underneath, in the shape of Poliwag's spiral.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, ice block, shadow, water, bubbles, glow, sparkles, frost mist or effects. One single creature, no extra views.

AVOID
- Not like Glimmora: no crystal flower, no petals of cut gemstones, no faceted jewels.
- Not an adult frog or toad: it stays a tadpole like Poliwag.
- No glossy 3D render, no plush or mascot look, no human features.
```

# Startprompt v2 (25 nov), na v1
v1: `r1/gemini_v1.png`. Jordi: "not bad, is het bewust dat er geen staart is? Verder ben ik bang dat dit teveel kleur en detail is en dat niet naar een sprite vertaalt". Daarna akkoord met: zuignap van het *Atelopus*-kikkervisje + plattere bouw (zuignap = buikvenster met de kring als rand), staart A (Poliwags staart: kern in lijfkleur, lichte/ijzige vin), max 2–3 kristallen, spiraal in één kleur (welke: open, Gemini kiest), één ijstint. Nieuw gesprek, bijlage alleen `bijlage_poliwag.png`.

```
Design a regional form of the Pokémon POLIWAG and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS THE NORMAL POLIWAG. Keep it clearly recognizable as Poliwag: round tadpole body, big eyes, small mouth, the two little feet, the spiral on the belly, and Poliwag's long thin TAIL.

THE TAIL IS REQUIRED. It sticks out to the side behind the body exactly like on the attached Poliwag: a thin core in the body color with a light, icy see-through fin around it.

CONCEPT
- Type Ice/Poison. A tadpole from cold, fast mountain streams in the Andes.
- Based on the tadpole of the harlequin toad (Atelopus), a small, very poisonous toad with bright warning colors. These tadpoles have a big round suction disc on the belly to cling to rocks in the current, and a somewhat flatter body.

DESIGN
- Main colors: the bright warning colors of a harlequin toad. Not blue like the normal Poliwag. Large simple color patches, no small spots.
- The belly is the suction disc: a round disc with a thick rim, made of clear ice. Through the ice you see Poliwag's spiral, in ONE single color. No rings or reflections in the ice.
- Only 2 or 3 small crystals: clear ice with red cinnabar inside, growing out of the skin. The animal comes first, the crystal second.
- Use one single ice color for everything icy (belly disc, tail fin, crystals).
- Keep the color count low and the details big enough to read at 64x64.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, ice block, shadow, water, bubbles, glow, sparkles, frost mist or effects. One single creature, no extra views.

AVOID
- No missing tail.
- Not like Glimmora: no crystal flower, no petals of cut gemstones, no faceted jewels.
- Not an adult frog or toad: it stays a tadpole like Poliwag.
- No glossy 3D render, no plush or mascot look, no human features.
```
