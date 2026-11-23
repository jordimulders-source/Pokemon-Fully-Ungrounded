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
