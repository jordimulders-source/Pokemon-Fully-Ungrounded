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
