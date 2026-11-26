# Gemini-prompt: gaucho-Lotad, startprompt v1 (25 nov)

Regels: `docs/lessen/GEMINI.md`. Geen bijlage. Besluiten Jordi: `../SPEC.md`.
Voorstel Claude (niet door Jordi gezegd, schrappen bij twijfel): het blad op het hoofd vormt de hoed; de gaucho in Lotad blijft klein (Jordi: gaucho in elke fase "alleen met een goed idee"), Gemini mag het verder ontwerpen. Kleur en pose kiest Gemini vrij.

```
Design a regional form of the Pokémon LOTAD and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A plant that IS a gaucho (the cowboy of the South American pampas, known for his wide hat).
- Type: Ground. It is NOT a Water or Grass type and does not live in water.
- The gaucho look comes only from the plant's own body parts. The leaf on its head forms the gaucho hat.
- This is the first, smallest stage of its line: small, simple, cute, still mostly a little plant creature.

DESIGN
- Keep Lotad's basic build: a small round body with a large leaf on top and short little legs underneath.
- Design the rest freely so that it reads as a small plant-gaucho.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Compact silhouette, limbs close to the body.
- Plain white background. No floor, rock, soil, shadow, water, glow, sparkles or effects. One single creature, no extra views.

AVOID
- NO clothing and NO accessories: no poncho, scarf, belt, boots, spurs, knife, whip, lasso, bolas, mate cup, no real hat on top of the leaf.
- Not a human, not a person in a plant costume.
- No glossy 3D render, no plush or mascot look.
```

# Startprompt v2 (25 nov), na r1
Jordi over r1: "tof idee, dit gaat werken"; "hij wijkt iets teveel van lotad af"; "Hij heeft ook 2 armen en 4 poten"; daarna: "lotad heeft 6 poten", "wist ik niet", "dan zeg ik niks" ; toen: "probeer 1 prompt dat die meer op 6 poten staat", "ipv 4". Nieuw gesprek, bijlage `bijlage_lotad.png` (Lotads eigen Gen 3-sprite, 8×; voor bouw en gezicht). Hoedbeschrijving = wat r1 had (plat blad met opstaande rand); 6 poten, geen armen (r1 had 2 armen en 4 poten).

```
Design a regional form of the Pokémon LOTAD and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS LOTAD. Stay very close to it: same build, same proportions, same angle, same face with the duck bill. Only the changes below are different.

CONCEPT
- A plant that IS a gaucho (the cowboy of the South American pampas, known for his wide hat).
- Type: Ground. It is NOT a Water or Grass type and does not live in water.
- The gaucho look comes only from the plant's own body parts: Lotad's leaf on its head IS the gaucho hat, a flat round leaf with a raised rim like a wide hat brim.
- First, smallest stage of its line: small, simple, still mostly a little plant creature.

BUILD (most important)
- Exactly Lotad's build: the big leaf-hat covers most of the creature; the small body sits underneath it and only a little of it shows.
- It stands on SIX short stubby legs under the body, like Lotad (not four). No arms: all six limbs are legs that stand on the ground.
- The leaf is clearly wider than the body, like Lotad's.

POSE
- Three-quarter view facing left, like the attached sprite.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, soil, shadow, water, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No arms, no hands, not four legs.
- NO clothing and NO accessories: no poncho, scarf, belt, boots, spurs, knife, whip, lasso, bolas, mate cup, no real hat on top of the leaf.
- Not green and blue like the normal Lotad. Not a human, not a person in a plant costume.
- No glossy 3D render, no plush or mascot look.
```

# Startprompt v3 (25 nov), na r2
Jordi over r2 (v2 met Lotad-bijlage): "veel minder op alle fronten". Terug naar v1 (gaf r1, "tof idee"), alleen de twee punten erbij: dichter bij Lotads verhoudingen en 6 poten zonder armen. Geen bijlage.

```
Design a regional form of the Pokémon LOTAD and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A plant that IS a gaucho (the cowboy of the South American pampas, known for his wide hat).
- Type: Ground. It is NOT a Water or Grass type and does not live in water.
- The gaucho look comes only from the plant's own body parts. The leaf on its head forms the gaucho hat.
- This is the first, smallest stage of its line: small, simple, cute, still mostly a little plant creature.

DESIGN
- Keep Lotad's basic build and proportions: a small, low body almost hidden under a large leaf that is much wider than the body.
- It stands on SIX short stubby legs, like Lotad. No arms.
- Design the rest freely so that it reads as a small plant-gaucho.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Compact silhouette, limbs close to the body.
- Plain white background. No floor, rock, soil, shadow, water, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No arms, no hands, not four legs.
- NO clothing and NO accessories: no poncho, scarf, belt, boots, spurs, knife, whip, lasso, bolas, mate cup, no real hat on top of the leaf.
- Not a human, not a person in a plant costume.
- No glossy 3D render, no plush or mascot look.
```

# Bijstuurprompt v4 (25 nov), na r3
Jordi over r3 (v3): "dit klopt niet, het is nu gewoon een semi pallette swap, er zit geen gaucho meer in". "Lotads verhoudingen" in tekst of bijlage trekt Gemini naar een kopie. Daarom: r1 als basis (in het r1-gesprek, of nieuw gesprek met `r1/gemini_r1.png` als bijlage), alleen 2 wijzigingen (les GEMINI.md: max. 1–2 per bijlageronde).

```
The attached image is my design. Keep EVERYTHING exactly the same: the hat-shaped leaf with the curled brim, the colors, the stern face, the bill, the style.
Change ONLY these two things:
1. Remove the two arms. It has no arms at all.
2. It stands on SIX short stubby legs (three on each side), close under the body.
Keep it a 64x64 Gen 3 front sprite on a plain white background.
```

# Bijstuurprompt v5 (25 nov), na r4
Jordi over r4 (armen weg, nog 4 poten): "nu is die geamputeerd". Zelfde gesprek, nog één bijsturing; lukt het niet, dan plakt Claude twee bestaande poten bij in het model.

```
Good, keep this exactly. Now it looks like something is missing below the body. Fix ONLY the legs:
It must have SIX legs in total, all the same short stubby size, spread evenly in a ring around the bottom of its round body, like a small beetle or like Lotad: two at the front, two in the middle, two at the back. The legs fill the space under the body so nothing looks cut off.
Keep everything else exactly the same.
```

# Startprompt v6 (25 nov), na r5
Jordi: "we kunnen r1 doen, maar dat ontwerp heeft teveel detail voor een sprite"; "nieuwe prompt maar dan? Anders vertaalt dat niet". Basis = v1 (gaf r1), met r1's ontwerp in eenvoudige woorden + weinig detail + 6 poten zonder armen. Nieuw gesprek, geen bijlage.
Keuze Claude (schrappen bij twijfel): het rafelige "bastkraagje" van r1 als één effen donkerdere onderhelft beschreven, zonder zigzag/rafels; krulletjes/barsten/textuur verboden.

```
Design a regional form of the Pokémon LOTAD and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A plant that IS a gaucho (the cowboy of the South American pampas, known for his wide hat).
- Type: Ground. It is NOT a Water or Grass type and does not live in water.
- The gaucho look comes only from the plant's own body parts. The leaf on its head forms the gaucho hat.
- This is the first, smallest stage of its line: small, simple, still mostly a little plant creature.

DESIGN
- On its head: a big, flat, round leaf in terracotta / clay-brown with a raised rim, so it reads clearly as a wide-brimmed hat. Wider than the body.
- Under it: a small round body in warm red-brown with a yellow duck bill and stern, frowning eyes (a tough little cowboy look).
- The lower half of the body is a plain, darker earthy olive-brown.
- It stands on SIX short stubby legs (three on each side) close under the body. No arms.

SIMPLE, FEW DETAILS (important)
- Big clear shapes that read well at 64x64, like Lotad's own sprite.
- Smooth flat surfaces with simple Gen 3 shading only: no cracks or veins on the leaf, no curls on the rim, no fringe, no zigzag pattern, no bark or fur texture.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Compact silhouette, limbs close to the body.
- Plain white background. No floor, rock, soil, shadow, water, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No arms, no hands, not four legs.
- NO clothing and NO accessories: no poncho, scarf, belt, boots, spurs, knife, whip, lasso, bolas, mate cup, no real hat on top of the leaf.
- Not green and blue like the normal Lotad. Not a human, not a person in a plant costume.
- No glossy 3D render, no plush or mascot look.
```

# Startprompt v7 (25 nov) = v1 + één regel eenvoud
Jordi: "ik vind het ontwerp nu prima dat die maar op 4 poten staat"; "pas gewoon je r1 prompt aan dat het design zo blijft maar wat makkelijker te vertalen naar een sprite". v1 letterlijk; alleen in STYLE AND FORMAT één regel erbij. Nieuw gesprek, geen bijlage.

```
Design a regional form of the Pokémon LOTAD and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A plant that IS a gaucho (the cowboy of the South American pampas, known for his wide hat).
- Type: Ground. It is NOT a Water or Grass type and does not live in water.
- The gaucho look comes only from the plant's own body parts. The leaf on its head forms the gaucho hat.
- This is the first, smallest stage of its line: small, simple, cute, still mostly a little plant creature.

DESIGN
- Keep Lotad's basic build: a small round body with a large leaf on top and short little legs underneath.
- Design the rest freely so that it reads as a small plant-gaucho.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Keep the details few and bold, like a real Gen 3 sprite: big readable shapes, no fine patterns or tiny textures.
- Compact silhouette, limbs close to the body.
- Plain white background. No floor, rock, soil, shadow, water, glow, sparkles or effects. One single creature, no extra views.

AVOID
- NO clothing and NO accessories: no poncho, scarf, belt, boots, spurs, knife, whip, lasso, bolas, mate cup, no real hat on top of the leaf.
- Not a human, not a person in a plant costume.
- No glossy 3D render, no plush or mascot look.
```
