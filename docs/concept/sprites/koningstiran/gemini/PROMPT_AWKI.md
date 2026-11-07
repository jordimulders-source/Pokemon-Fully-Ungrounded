# Gemini-prompts: koningstiran fase 2 "awki" (7 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn: `docs/concept/POKEMON.md` (Koningstiran-lijn). Fase 1: `../../hatun_runa/af/hatun_runa_8x.png`, fase 3: `bijlage_sapa_inca_6x.png`.

## Besloten (Jordi, 7 nov)
- Vogel: **koningstiran met gesloten kuif** (de "hamerkop"). Niet de vuurtiran: "vuurtiran is wat kleiner dan de koningstiran, al heeft die niet de kuif die ik juist een heel goed idee vind".
- Experiment met twee versies: **A** = vuur in de kuif, **B** = vuur als vleugelpatroon van **trapdriehoeken** ("trapdriehoeken voor vleugelpatroon is geniaal").
- In beide: gele franje (kroonprins) en kleine gouden oorvlekken; de bouw van de caracara begint (langere poten, rechter dan fase 1).
- Pose (keuze Claude, Jordi kan bijsturen): net geland, nabije vleugel nog half open; kop driekwart naar de kijker. Gelijk in A en B zodat ze vergelijkbaar zijn; B heeft de open vleugel nodig om het patroon te tonen.

## Bijlagen (beide prompts, in deze volgorde)
1. `../../hatun_runa/af/hatun_runa_8x.png` (fase 1)
2. `bijlage_sapa_inca_6x.png` (fase 3)
3. Een foto van een **koningstiran met gesloten kuif** (*Onychorhynchus coronatus*, Royal flycatcher). Jordi zoekt er een; daarna opslaan als `../referenties/koningstiran_dicht_foto.*`.

Elke prompt in een **eigen nieuw gesprek**.

## Prompt A: vuur in de kuif

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is the FIRST stage of this 3-stage bird line (a Great kiskadee, a common city bird).
- Attachment 2 is the FINAL stage: the Inca emperor (Sapa Inca), with a huge open fan crown.
- Attachment 3 is a photo of the real animal for THIS stage: a Royal flycatcher (Onychorhynchus coronatus) with its crest CLOSED.
- Use attachments 1 and 2 only for palette and family resemblance. Do NOT copy the fan crown, staff, large ear discs, pose or size of attachment 2.

THE CREATURE
- The SECOND stage, Fire/Flying: the crown prince (in Quechua "awki"). Not yet a king; a proud young heir between the humble first stage and the emperor.
- Anatomy: a Royal flycatcher. Its crest is CLOSED and lies flat backwards over the head as one long, flat, pointed shape sticking out far behind the back of the head, like a hammerhead. This closed crest is the main feature of the design and must be clearly readable in the silhouette.
- The build starts growing towards the final stage: a bit taller and more upright than stage 1, longer legs, but still a medium-sized bird, not yet big and heavy.
- Body: warm dark brown back and wings, golden-ochre belly, rust-brown tail, broad flat dark beak.

THE FIRE (only in the crest)
- The closed crest is where the fire lives: the folded crest feathers are flame red and orange, getting brighter towards the tip, with the edges and the tip glowing yellow like a smouldering ember. It is still folded shut: the fire is held in, waiting to burst open in the next stage.
- No flames anywhere else on the body. The wings and tail are plain brown with rust-brown edges.

THE INCA REFERENCES (feathers only, nothing more)
- In the Inca empire the crown prince wore a YELLOW fringe on the forehead (the emperor's was red). On this bird: a short fringe of yellow feathers hanging over the base of the beak, between the eyes.
- Noble Inca youths received gold ear plugs at their initiation. On this bird: a small round gold patch of feathers on each side of the head, behind the eye. Small; they become large discs only in the final stage.
- No clothing, jewelry, staff, patterns on the chest or anything else.

POSE AND VIEW
- It has just landed: standing on its own legs, body upright in 3/4 view facing left, near wing still half open as it folds in, far wing folded.
- Head in 3/4 view towards the viewer: both eyes visible, beak pointing left-down, the long closed crest sticking out behind the head to the right.
- Proud and alert, a little arrogant; not angry, not sleepy.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO branch, perch, ground, rock, shadow or base.
- No glow aura, sparkles, loose flames, smoke, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Fletchinder, Talonflame, Moltres, Ho-Oh, Pidgeotto, Swellow, Staravia, Corviknight or Oricorio.
- Not a woodpecker, not a cardinal, no upright crest; the crest lies flat and points backwards.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes. It is a wild animal that looks like a Pokémon.
```

## Prompt B: vuur als vleugelpatroon (trapdriehoeken)

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is the FIRST stage of this 3-stage bird line (a Great kiskadee, a common city bird).
- Attachment 2 is the FINAL stage: the Inca emperor (Sapa Inca), with a huge open fan crown.
- Attachment 3 is a photo of the real animal for THIS stage: a Royal flycatcher (Onychorhynchus coronatus) with its crest CLOSED.
- Use attachments 1 and 2 only for palette and family resemblance. Do NOT copy the fan crown, staff, large ear discs, pose or size of attachment 2.

THE CREATURE
- The SECOND stage, Fire/Flying: the crown prince (in Quechua "awki"). Not yet a king; a proud young heir between the humble first stage and the emperor.
- Anatomy: a Royal flycatcher. Its crest is CLOSED and lies flat backwards over the head as one long, flat, pointed shape sticking out far behind the back of the head, like a hammerhead. This closed crest is the main feature of the silhouette. Its color is golden yellow with a darker rust tip, no fire.
- The build starts growing towards the final stage: a bit taller and more upright than stage 1, longer legs, but still a medium-sized bird, not yet big and heavy.
- Body: warm dark brown back and wings, golden-ochre belly, rust-brown tail, broad flat dark beak.

THE FIRE (only as a wing pattern)
- The fire is a woven Andean pattern on the wing coverts: one or two rows of STEPPED TRIANGLES (the classic Andean "escalonado" motif: triangles with stair-step edges instead of straight diagonal sides), all pointing up, like a row of flames.
- Each stepped triangle goes from dark red at the base through orange to yellow at the tip. Clean geometric pixel steps, the same shape repeated, like a textile border; not random flames, not loose symbols.
- The pattern is part of the feathers, not a cloth or an armband. Flight feathers and tail stay plain brown with rust-brown edges. No fire on the head.

THE INCA REFERENCES (feathers only, nothing more)
- The stepped-triangle wing pattern described above.
- In the Inca empire the crown prince wore a YELLOW fringe on the forehead (the emperor's was red). On this bird: a short fringe of yellow feathers hanging over the base of the beak, between the eyes.
- Noble Inca youths received gold ear plugs at their initiation. On this bird: a small round gold patch of feathers on each side of the head, behind the eye. Small; they become large discs only in the final stage.
- No clothing, jewelry, staff, patterns on the chest or anything else.

POSE AND VIEW
- It has just landed: standing on its own legs, body upright in 3/4 view facing left, near wing still half open as it folds in so the stepped-triangle pattern is clearly visible, far wing folded.
- Head in 3/4 view towards the viewer: both eyes visible, beak pointing left-down, the long closed crest sticking out behind the head to the right.
- Proud and alert, a little arrogant; not angry, not sleepy.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO branch, perch, ground, rock, shadow or base.
- No glow, sparkles, real flames, smoke, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Fletchinder, Talonflame, Moltres, Ho-Oh, Pidgeotto, Swellow, Staravia, Corviknight or Oricorio.
- Not a woodpecker, not a cardinal, no upright crest; the crest lies flat and points backwards.
- No Aztec/Mexican or Japanese look; no zigzag lightning bolts; no Native North American feather headdress.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes. It is a wild animal that looks like a Pokémon.
```

Bijsturen (max. 1–2 keer, één zin), bijv. `same design, make the closed crest longer and flatter` of `same design, stepped triangles bigger and fewer`.

## Startprompts v2 (7 nov, nieuw gesprek per prompt; vervangen A en B hierboven)
Na ronde 1 (Jordi: "heel rare kop" / "net pidgeot met een heel matig patroontje"; "de kuif moet verticaler en korter"). Wijzigingen: kuif ±kop-lang, vast uit de kruin, schuin naar achteren-boven (30–45°) als gesloten waaier; gezicht van fase 1 (zwart masker, witte keel) blijft; gewone snavel; kop meer naar de kijker; trapdriehoeken uitgelegd als blokpiramides; Pidgeot met name vermeden.
Bijlagen: 1 = `../../hatun_runa/af/hatun_runa_8x.png`, 2 = `bijlage_sapa_inca_6x.png` (eventueel 3 = foto koningstiran).

### Prompt A v2: vuur in de kuif
```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is the FIRST stage of this 3-stage bird line (a Great kiskadee).
- Attachment 2 is the FINAL stage: the Inca emperor (Sapa Inca), with a huge open fan crown.
- I need the SECOND stage in between. Use the attachments for palette and family resemblance only. Do NOT copy the open fan crown, staff, large ear discs or pose of attachment 2.

THE CREATURE
- Second stage, Fire/Flying: the crown prince (Quechua "awki"). A proud young heir, not yet a king. Based on the Royal flycatcher (Onychorhynchus coronatus), whose crown is a fan that is usually kept folded shut.
- HEAD (most important): keep the face of attachment 1: black mask through the eye, white throat, short straight sturdy dark beak (like attachment 1, NOT flat or duck-like). The head is turned towards the viewer in 3/4 view: both eyes visible, beak pointing left-down.
- CREST: a FOLDED fan crest that grows out of the top of the head, part of the head itself, not lying on top of it like a hat. It is short (about as long as the head) and narrow, pointing backwards and UPWARDS at about 40 degrees, like a closed hand fan waiting to open. Not long, not flowing, not flat.
- Build: a bit taller and more upright than stage 1, slightly longer legs, still medium-sized.
- Body: warm dark brown back and wings, golden-ochre belly, rust-brown tail.

THE FIRE (only in the crest)
- The folded crest is flame red and orange, brighter towards the tip, with the edges and tip glowing yellow like an ember. The fire is held in the closed fan; it bursts open in the next stage.
- No fire anywhere else. Wings and tail plain brown with rust-brown edges.

INCA DETAILS (feathers only)
- A short row of small yellow feathers on the forehead just above the beak (the crown prince's yellow fringe). Small, neat, NOT hair, NOT bangs, NOT a beard.
- A small round gold feather patch behind each eye (the young noble's first ear plugs).
- Nothing else: no clothing, jewelry, staff or chest pattern.

POSE
- Standing on its own legs, body in 3/4 view facing left, chest out, near wing half open as it just landed, far wing folded. Proud and alert, a little arrogant.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO branch, ground, shadow or base. No glow aura, loose flames, smoke, sparkles, text or effects. One single creature.

AVOID
- NOT Pidgeot or Pidgeotto: no long flowing head plume, no plain brown profile bird.
- Not Fletchinder, Talonflame, Moltres, Ho-Oh, a cardinal or a woodpecker.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```

### Prompt B v2: trapdriehoeken op de vleugel
```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is the FIRST stage of this 3-stage bird line (a Great kiskadee).
- Attachment 2 is the FINAL stage: the Inca emperor (Sapa Inca), with a huge open fan crown.
- I need the SECOND stage in between. Use the attachments for palette and family resemblance only. Do NOT copy the open fan crown, staff, large ear discs or pose of attachment 2.

THE CREATURE
- Second stage, Fire/Flying: the crown prince (Quechua "awki"). A proud young heir, not yet a king. Based on the Royal flycatcher (Onychorhynchus coronatus), whose crown is a fan that is usually kept folded shut.
- HEAD (most important): keep the face of attachment 1: black mask through the eye, white throat, short straight sturdy dark beak (like attachment 1, NOT flat or duck-like). The head is turned towards the viewer in 3/4 view: both eyes visible, beak pointing left-down.
- CREST: a FOLDED fan crest that grows out of the top of the head, part of the head itself, not lying on top of it like a hat. It is short (about as long as the head) and narrow, pointing backwards and UPWARDS at about 40 degrees, like a closed hand fan waiting to open. Golden yellow with a rust-red tip. Not long, not flowing, not flat.
- Build: a bit taller and more upright than stage 1, slightly longer legs, still medium-sized.
- Body: warm dark brown back and wings, golden-ochre belly, rust-brown tail.

THE FIRE (only as a wing pattern)
- On the near wing, across the wing coverts: ONE row of 3 or 4 BIG stepped triangles pointing up, like flames. Each triangle is a stepped pyramid built from stacked blocks: a wide block at the bottom, a narrower block on top of it, and the narrowest block at the tip, so the sides go up in clear stairs, never as straight diagonal lines. This is the Andean "escalonado" textile motif.
- Each stepped triangle: dark red bottom block, orange middle block, yellow top block. All triangles the same shape, evenly spaced, large enough to read clearly at sprite size.
- It is part of the feathers, not cloth or an armband. Flight feathers and tail plain brown with rust-brown edges. No fire on the head.

INCA DETAILS (feathers only)
- The stepped-triangle wing pattern above.
- A short row of small yellow feathers on the forehead just above the beak (the crown prince's yellow fringe). Small, neat, NOT hair, NOT bangs, NOT a beard.
- A small round gold feather patch behind each eye (the young noble's first ear plugs).
- Nothing else: no clothing, jewelry, staff or chest pattern.

POSE
- Standing on its own legs, body in 3/4 view facing left, chest out, near wing half open as it just landed so the stepped triangles are clearly visible, far wing folded. Proud and alert, a little arrogant.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO branch, ground, shadow or base. No glow, real flames, smoke, sparkles, text or effects. One single creature.

AVOID
- NOT Pidgeot or Pidgeotto: no long flowing head plume, no plain brown profile bird.
- Not Fletchinder, Talonflame, Moltres, Ho-Oh, a cardinal or a woodpecker.
- No sawtooth band, no zigzag, no Aztec/Mexican or Japanese look.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```

## Startprompt v3 (7 nov, nieuw gesprek; na r3 "hij loopt vast")
Bijlagen: 1 = `awki_r2_A_kuif.png` (basis), 2 = `awki_r3_A_bijgestuurd.png` (pose en patroon).

```
Draw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

- Attachment 1 is the base design. Keep its head, face, crest, ear patches, colors, body, legs and tail exactly as they are.
- Attachment 2 shows the pose and wing pattern I want. Take from it ONLY the raised wing with the big flame pattern. Attachment 2 has a mistake: it has three wings. Do not copy that.

ANATOMY (most important)
- The bird has exactly TWO wings.
- Near wing (on the right side of the body, closest to the viewer): raised up from the shoulder and reaching up and forward, feathers spread open, proudly greeting the sun like an Inca. This is the only raised wing and it carries the pattern.
- Far wing (on the left, behind the chest): folded and mostly hidden behind the body. No other wing anywhere.

THE PATTERN (on the raised wing only)
- 3 large stepped triangles pointing up, covering most of the wing coverts: dark red bottom, orange middle, yellow tip. Each triangle is a stepped pyramid made of stacked blocks, so its sides go up in clear stairs, never as smooth diagonal lines (Andean "escalonado" textile motif).

POSE
- Standing on its own legs, body in 3/4 view facing left, chest out, head lifted a little, beak pointing left. Proud, calm, a young prince.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. No ground, shadow, glow, sun, sparkles or effects. One single creature.
```
