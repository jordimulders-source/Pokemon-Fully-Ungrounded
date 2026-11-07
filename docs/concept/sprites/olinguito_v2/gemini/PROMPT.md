# Gemini-prompt: olinguito (Dark-starter fase 1), verbeterronde (7 nov)

Jordi (7 nov): "ik wil kijken of we bandingo kunnen verbeteren, toon me de sprite en schrijf een prompt voor gemini, om te kijken of hij er iets mooiers van kan maken" (bandingo = de olinguito).

Regels: `docs/lessen/GEMINI.md`. Huidige sprite: `../af/olinguito.png`; ontwerp: `../referenties/ONTWERP_GEKOZEN.png`; kenmerken: `../SPEC.md`.

## Bijlagen (in deze volgorde)
1. `bijlage_olinguito_6x.png` (de huidige sprite, 6×)
2. `bijlage_ontwerp.png` (het gekozen ontwerp)
3. eventueel `bijlage_coathief_6x.png` en `bijlage_wasbeer_6x.png` (fase 2 en 3, alleen familiegelijkenis)
4. eventueel een olinguitofoto (`../referenties/referentie_foto_boom.webp`)

## Prompt (in een nieuw gesprek plakken)

```
Draw an original Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is my current sprite of this Pokémon. Attachment 2 is its design drawing. Keep the same creature, pose and features, but make it a better, more polished sprite: cleaner shapes, better shading and more appeal, as if Game Freak drew it for Ruby/Sapphire.
- Attachments 3 and 4 (if present) are its 2nd and 3rd evolution (a coati and a crab-eating raccoon). Use them only for family resemblance. Do NOT copy their mask, balaclava, bag or pose.

THE CREATURE
- First stage of a Dark-type starter line from a South American region. A small thief that will grow into a vigilante.
- Anatomy: the olinguito (Bassaricyon neblina), a small cloud-forest relative of the raccoon: round head, small round ears, short pointed snout, dense dark brown fur, long thin tail.
- Head: grey-brown face, warm brown fur only on the back of the head, a black mask band across the eye like Zigzagoon, stopping just behind the eye. One small dark red-brown eye inside the mask (sinister, not bright red). Snout dark grey-brown, separate from the mask, with a dusty pink nose.
- Ears: one ear clearly visible (dark edge, lighter inside), the far ear barely visible.
- Body: dark brown, no belly patch. Front paws end in 2 long, light-colored claws each, like Linoone (larger than a real olinguito, the signature of this line). Pink feet.
- Tail: long and thin, curving up behind the body and bending back at the tip.
- Mood: cute and sinister at the same time. Not comical.

POSE AND VIEW
- The same pose as attachment 1: low on all fours, moving left like Linoone, head low and turned in 3/4 towards the viewer, only one eye visible, near front paw reaching forward with the claws, back legs asymmetric (one pulled under the body, one pushing off), tail up.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO branch, rock, ground, shadow or base. No glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Do not make it look like Zigzagoon, Linoone, Sentret, Furret, Purrloin, Meowth or a monkey.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
- No clothing, bag, bandana or accessories.
```

## Tips voor Jordi
- Gemini maakt geen echte 64×64; het plaatje is het nieuwe ontwerp, de maker-agent vertaalt het daarna naar de sprite.
- Bijsturen hooguit 1–2 keer met één zin (bijv. `same design, only make the claws longer`). Daarna een nieuw gesprek met de beste versie als bijlage.
- Vraag niet om "cuter" of "more Pokémon": dan glijdt hij naar bekende soorten.

## Ronde 1 (7 nov): afgekeurd
`ronde1_afgekeurd.png`. Jordi: "dat is niet beter, amper aangepast, behalve het hoofd wat ik juist goed vond".

## Startprompt v2 (7 nov, nieuw gesprek)
Jordi: "juist de pose en features moeten wat beter"; het hoofd vond hij goed. Bijlagen: 1 = `bijlage_kop_8x.png` (alleen de kop), 2 = `../referenties/referentie_foto_boom.webp`, 3 = `../referenties/referentie_foto_voor.png`. De hele huidige sprite niet meesturen.

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is the HEAD of this Pokémon, from my current sprite. Keep this head exactly: its shape, grey-brown face, warm brown back of the head, black mask band across the eye, small dark red-brown eye, dark grey-brown snout, dusty pink nose, one dominant ear. Do not redesign the head.
- Attachments 2 and 3 are photos of the real animal, the olinguito (Bassaricyon neblina). Use them for the anatomy of the body, legs, paws and tail.

WHAT TO DESIGN (everything except the head is open)
- A better pose and better body features than my current sprite. Design them freshly. Make the pose more dynamic and more appealing, with a clear, readable silhouette.
- The body, legs, paws, claws and tail are yours to design, within these rules:
  - Real olinguito anatomy: slim, dense dark brown fur, no belly patch, long thin tail (as long as the body or longer).
  - The signature of this line: 2 long, light-colored claws on each front paw, like Linoone (bigger than on a real olinguito). They must be clearly visible.
  - Pink feet.
- It is the first stage of a Dark-type starter line: a small thief that will grow into a vigilante. Cute and sinister at the same time, not comical.

VIEW
- Standard front-sprite view: the creature faces left, head in 3/4 towards the viewer, only one eye visible.
- The whole creature fits inside the frame.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO branch, tree, rock, ground, shadow or base. No glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Do not make it look like Zigzagoon, Linoone, Sentret, Furret, Purrloin, Meowth, a weasel, a ferret or a monkey.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
- No clothing, bag, bandana or accessories.
```

## Startprompt v3 (7 nov, nieuw gesprek; vervangt v2)
Jordi: "het hele concept is goed, alleen de afwerking niet zo, daarom wil ik kijken of dat met gemini beter kan". Concept, pose en kenmerken blijven; alleen de uitvoering moet beter. Bijlagen: 1 = `bijlage_ontwerp.png` (concept en pose), 2 = `bijlage_kop_8x.png` (kop, vast). De hele huidige sprite niet meesturen (r1: dan kopieert Gemini hem).

```
Redraw this Pokémon as a high-quality official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is the approved design: the creature, its pose and all its features. Keep all of it. Do not change the concept, the pose or the proportions.
- Attachment 2 is the head from my current sprite. Keep this head exactly as it is in the sprite (shape, colors, black mask band, small dark red-brown eye, pink nose, one dominant ear).

THE TASK
- My current sprite has the right design but weak craftsmanship. Draw it again from scratch, from attachment 1, at the level of a professional Game Freak sprite artist. The improvement must be in the execution, not in the design:
  - Clear, confident anatomy: the shoulder, elbow, knee and heel of each leg are readable; legs have weight and volume, not flat sticks.
  - Paws and claws drawn with care: the 2 long light claws per front paw are clean, separate and sharp, attached to the paw; pink feet with clear toes.
  - The tail tapers smoothly and has volume and fur shading along its whole length.
  - Shading that shows the round form of the body (light from top left, shadow underneath), with clean color clusters, no noise, no pillow shading.
  - A clean, smooth 1 px outline with no jaggies, darker on the shadow side.
- It is an olinguito (Bassaricyon neblina), the first stage of a Dark-type starter line: cute and sinister at the same time.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, light from top left.
- Plain white background. NO branch, rock, ground, shadow or base. No glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Do not redesign it. Do not make it look like Zigzagoon, Linoone, Sentret, Furret, Purrloin, a ferret or a monkey.
- No plush toy, chibi or mascot look; no oversized sparkly eyes. No clothing or accessories.
```
