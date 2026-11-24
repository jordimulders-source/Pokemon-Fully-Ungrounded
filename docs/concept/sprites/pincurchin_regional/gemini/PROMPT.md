# Gemini-prompt: regionale Pincurchin, startprompt v1 (23 nov)

Regels: `docs/lessen/GEMINI.md`. Bijlage: `bijlage_pincurchin.png` (Pincurchins eigen sprite, 8×; alleen voor het gezicht).
Jordi: zie `../SPEC.md` (Poison/Rock; "hybride, lijkend op een soort onderwater mijn"; "Pincurchins gezicht").
Kleur en pose heeft Jordi niet genoemd: Gemini kiest vrij; kiezen we daarna. AVOID-regels over bom/ketting/anker/klinknagels/schedel zijn voorstel Claude (zodat het een Pokémon blijft en geen voorwerp).

```
Design a regional form of the Pokémon PINCURCHIN and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS PINCURCHIN. Copy its face exactly: the yellow eyes and the orange teeth/mouth, same shape and same place low on the front of the body.

CONCEPT
- A hybrid of a pencil-spined sea urchin and an old underwater naval mine (sea mine).
- Type Poison/Rock. It should look sinister.

DESIGN
- Body: a round sea-mine body that is also an urchin shell.
- Spines: the thick, blunt, pencil-like spines of a pencil sea urchin, placed around the body the way the contact horns sit on a sea mine.
- Face: Pincurchin's eyes and teeth from the attachment.
- Colors that suit a Poison/Rock Pokémon.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, shadow, water, bubbles, glow, sparkles or effects. One single creature, no extra views.

AVOID
- Not a cartoon bomb with a fuse, no chains, no anchor, no metal bolts or rivets, no skull.
- No arms, legs or human features. No glossy 3D render, no plush or mascot look.
- Not thin needle spines like the normal Pincurchin.
```

# Startprompt v2 (23 nov), na v1
Jordi over v1: "de stekels moeten groter, ik dacht aan bruin voor de binnenkant en donkerrood voor de stekels, geen roest". Nieuw gesprek, bijlage alleen `bijlage_pincurchin.png`.

```
Design a regional form of the Pokémon PINCURCHIN and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS PINCURCHIN. Copy its face exactly: the yellow eyes and the orange teeth/mouth, same shape and same place low on the front of the body.

CONCEPT
- A hybrid of a pencil-spined sea urchin and an old underwater naval mine (sea mine).
- Type Poison/Rock. It should look sinister.

DESIGN
- Body: a round sea-mine body that is also an urchin shell. The body is brown.
- Spines: BIG spines, the thick, blunt, pencil-like spines of a pencil sea urchin, placed around the body the way the contact horns sit on a sea mine. The spines are dark red.
- Face: Pincurchin's eyes and teeth from the attachment.
- Clean colors: NO rust, no rust spots or stains.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, shadow, water, bubbles, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No rust. Not a cartoon bomb with a fuse, no chains, no anchor, no metal bolts or rivets, no skull.
- No arms, legs or human features. No glossy 3D render, no plush or mascot look.
- Not thin needle spines like the normal Pincurchin. Not small spines.
```

# Startprompt v3 (23 nov), na v2
Jordi over v2: "de ogen zijn anders maar dat is niet erg, ik vind hem verder te kaal" · "en het rood mag wat feller" · "wel donker". "Te kaal" letterlijk doorgegeven. Nieuw gesprek, bijlage alleen `bijlage_pincurchin.png`.

```
Design a regional form of the Pokémon PINCURCHIN and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS PINCURCHIN. Use its face: the yellow eyes and the orange teeth/mouth, low on the front of the body.

CONCEPT
- A hybrid of a pencil-spined sea urchin and an old underwater naval mine (sea mine).
- Type Poison/Rock. It should look sinister.

DESIGN
- Body: a round sea-mine body that is also an urchin shell. The body is brown.
- Spines: BIG spines, the thick, blunt, pencil-like spines of a pencil sea urchin, placed around the body the way the contact horns sit on a sea mine.
- Spine color: a dark red, but more vivid and saturated (a brighter red that is still dark), not a dull brownish red.
- Face: Pincurchin's eyes and teeth from the attachment.
- Clean colors: NO rust, no rust spots or stains.
- It must NOT look too bare or plain.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, shadow, water, bubbles, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No rust. Not a cartoon bomb with a fuse, no chains, no anchor, no metal bolts or rivets, no skull.
- No arms, legs or human features. No glossy 3D render, no plush or mascot look.
- Not thin needle spines like the normal Pincurchin. Not small spines. Not bare or plain.
```

# Startprompt v4 (23 nov), vervangt v3
Jordi over "te kaal": "de stekels bedekken niet genoeg van het lijf, te kort, niet genoeg, misschien wel allebei". Nieuw gesprek, bijlage alleen `bijlage_pincurchin.png`.

```
Design a regional form of the Pokémon PINCURCHIN and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS PINCURCHIN. Use its face: the yellow eyes and the orange teeth/mouth, low on the front of the body.

CONCEPT
- A hybrid of a pencil-spined sea urchin and an old underwater naval mine (sea mine).
- Type Poison/Rock. It should look sinister.

DESIGN
- Body: a round sea-mine body that is also an urchin shell. The body is brown.
- Spines: the thick, blunt, pencil-like spines of a pencil sea urchin. MANY spines and LONG spines: they must cover much more of the body, so only parts of the brown body show between them. Spines all over the body, also in front of the body pointing toward the viewer, not only along the outline.
- Spine color: a dark red, but more vivid and saturated (a brighter red that is still dark), not a dull brownish red.
- Face: Pincurchin's eyes and teeth from the attachment, still clearly visible between the spines.
- Clean colors: NO rust, no rust spots or stains.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, shadow, water, bubbles, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No rust. Not a cartoon bomb with a fuse, no chains, no anchor, no metal bolts or rivets, no skull.
- No arms, legs or human features. No glossy 3D render, no plush or mascot look.
- Not thin needle spines like the normal Pincurchin. Not short spines, not few spines, not a bare body.
```

# Bijsturen v4 → v5 (23 nov), in hetzelfde gesprek
Jordi over v4: "beter, maar het steen heeft teveel detail". Eén wijziging, dus bijsturen i.p.v. nieuw gesprek.

```
Keep everything exactly the same (spines, colors, face, pose). Only change one thing: the brown stone body has too much detail. Make the brown body simpler and smoother, with clean Gen 3 shading and no extra lumps, cracks, bumps or texture on it.
```

# Startprompt v5 (23 nov), vervangt de bijstuurzin
Jordi: "beter, maar het steen heeft teveel detail" · "hij lijkt ook steeds minder op pincurchin" · keuze "Gezicht exact". Nieuw gesprek, bijlage alleen `bijlage_pincurchin.png`.

```
Design a regional form of the Pokémon PINCURCHIN and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS PINCURCHIN. COPY ITS FACE EXACTLY, pixel for pixel: the two round yellow eyes with a dark pupil, set far apart, and the orange teeth/mouth between them, low on the front of the body. Same shapes, same sizes, same colors, same positions as in the attachment. Do not redesign the eyes (no eyebrows, no angry or slanted eyes) and do not redesign the mouth.

CONCEPT
- A hybrid of a pencil-spined sea urchin and an old underwater naval mine (sea mine).
- Type Poison/Rock. It should look sinister.

DESIGN
- Body: a round sea-mine body that is also an urchin shell. The body is brown and SIMPLE: smooth, with clean Gen 3 shading, no lumps, cracks, bumps, ridges or texture.
- Spines: the thick, blunt, pencil-like spines of a pencil sea urchin. MANY spines and LONG spines: they must cover much more of the body, so only parts of the brown body show between them. Spines all over the body, also in front of the body pointing toward the viewer, not only along the outline.
- Spine color: a dark red, but more vivid and saturated (a brighter red that is still dark), not a dull brownish red.
- The face stays clearly visible between the spines.
- Clean colors: NO rust, no rust spots or stains.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, shadow, water, bubbles, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No rust, no texture or detail on the stone body. Not a cartoon bomb with a fuse, no chains, no anchor, no metal bolts or rivets, no skull.
- No eyebrows, no changed eyes or mouth. No arms, legs or human features. No glossy 3D render, no plush or mascot look.
- Not thin needle spines like the normal Pincurchin. Not short spines, not few spines, not a bare body.
```

# Startprompt v6 (23 nov), na v5
Jordi (v5 naast foto pencil urchin): "behoorlijk verschil nog wel" · "dunner, langer en dichtheid, maar het gezicht mag daarvan utigezonderd zijn". Nieuw gesprek, bijlage alleen `bijlage_pincurchin.png` (foto niet meesturen, GEMINI.md). "thick" en de AVOID-regel tegen dunne stekels zijn weg.

```
Design a regional form of the Pokémon PINCURCHIN and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS PINCURCHIN. COPY ITS FACE EXACTLY, pixel for pixel: the two round yellow eyes with a dark pupil, set far apart, and the orange teeth/mouth between them, low on the front of the body. Same shapes, same sizes, same colors, same positions as in the attachment. Do not redesign the eyes (no eyebrows, no angry or slanted eyes) and do not redesign the mouth.

CONCEPT
- A hybrid of a pencil-spined sea urchin and an old underwater naval mine (sea mine).
- Type Poison/Rock. It should look sinister.

DESIGN
- Body: a round sea-mine body that is also an urchin shell. The body is brown and SIMPLE: smooth, with clean Gen 3 shading, no lumps, cracks, bumps, ridges or texture.
- Spines: the pencil-like spines of a pencil sea urchin. THINNER, LONGER and MUCH DENSER than usual: many long, slender spines packed closely together, radiating out from the body in all directions, covering most of the body.
- The face area is the exception: no spines in front of the face, so the eyes and mouth stay fully visible.
- Spine color: a dark red, but vivid and saturated (a brighter red that is still dark), not a dull brownish red.
- Clean colors: NO rust, no rust spots or stains.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, shadow, water, bubbles, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No rust, no texture or detail on the stone body. Not a cartoon bomb with a fuse, no chains, no anchor, no metal bolts or rivets, no skull.
- No eyebrows, no changed eyes or mouth. No arms, legs or human features. No glossy 3D render, no plush or mascot look.
- Not short spines, not few spines, not thick cone-shaped spines, not a bare body.
```

# Startprompt v7 (23 nov), na v6
Jordi: "hij lijkt nog steeds niet, veel te stekelig" · keuze "Vorm: gladde staafjes". Nieuw gesprek, bijlage alleen `bijlage_pincurchin.png`.

```
Design a regional form of the Pokémon PINCURCHIN and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS PINCURCHIN. COPY ITS FACE EXACTLY, pixel for pixel: the two round yellow eyes with a dark pupil, set far apart, and the orange teeth/mouth between them, low on the front of the body. Same shapes, same sizes, same colors, same positions as in the attachment. Do not redesign the eyes (no eyebrows, no angry or slanted eyes) and do not redesign the mouth.

CONCEPT
- A hybrid of a pencil-spined sea urchin and an old underwater naval mine (sea mine).
- Type Poison/Rock. It should look sinister.

DESIGN
- Body: a round sea-mine body that is also an urchin shell. The body is brown and SIMPLE: smooth, with clean Gen 3 shading, no lumps, cracks, bumps, ridges or texture.
- Spines: exactly like the spines of a real red pencil sea urchin: SMOOTH, ROUND RODS, the same thickness along their whole length, with a BLUNT, ROUNDED end. Like long pencils or chopsticks. Thin, long and densely packed, each one clean and separate, all radiating neatly from the center of the body in all directions, covering most of the body.
- The face area is the exception: no spines in front of the face, so the eyes and mouth stay fully visible.
- Spine color: a dark red, but vivid and saturated (a brighter red that is still dark), not a dull brownish red.
- Clean colors: NO rust, no rust spots or stains.

POSE
- Three-quarter view facing left, like official Gen 3 front sprites.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No floor, rock, shadow, water, bubbles, glow, sparkles or effects. One single creature, no extra views.

AVOID
- NO pointed, sharp, jagged, serrated or shard-like spines, no spikes that taper to a point, no clusters of spikes.
- No rust, no texture or detail on the stone body. Not a cartoon bomb with a fuse, no chains, no anchor, no metal bolts or rivets, no skull.
- No eyebrows, no changed eyes or mouth. No arms, legs or human features. No glossy 3D render, no plush or mascot look.
- Not short spines, not few spines, not a bare body.
```

# Bijsturen v7 → v8 (23 nov), in hetzelfde gesprek als v7
Jordi: "ok veel beter, en hoe maken we hier nu een semi onderwater mijn nog van" · "bedenk maar een prompt". Kenmerken = voorstel Claude. Ogen/mond fixen we zelf in de sprite.

```
This is very good. Keep the spines, colors, body shape and pose exactly the same. Now make it look half like an old naval sea mine, with only these two additions:
1. Between the long red rods, add 4 to 6 SHORT, THICK sea-mine contact horns sticking out of the body: short stubby cylinders with a rounded, dome-shaped cap on the end, in a darker brown-grey than the body.
2. Add one horizontal seam around the middle of the body, like the welded joint where the two halves of a sea mine meet: a thin raised band that follows the curve of the ball. No rivets or bolts.
Do not add chains, an anchor, a fuse or a skull. Do not change the face.
```

Reserve (als het nog te weinig mijn is): "Add a small round ring on top of the body, like the lifting eye of a sea mine."
