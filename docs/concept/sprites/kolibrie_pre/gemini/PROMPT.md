# Gemini-prompt: Hummlet opknappen (opknapronde, 19 nov)

Regels: `docs/lessen/GEMINI.md`. Stand van de ronde: `../../OPKNAPRONDE_GEMINI.md`. Huidige sprite: `../af/kolibrie_pre.png`. Eindvorm Soulibri: `../../kolibrie/af/kolibrie.png` (niet als bijlage).

## Jordi (19 nov, letterlijk)
- "hummlet is net niet genoeg een hummingbird chick, maar heb ik toen maar opgegeven zodat we resultaat konden boeken."
- Opdracht: het model en design van de lijn blijven; Hummlet moet duidelijker een kolibriekuiken worden.
- Antwoorden op de vragen van Claude (19 nov):
  - Wat mist er (snavel / verhoudingen / vleugels / dons): eerst geen voorkeur, daarna: **"wat betreft vraag 1 alles, maar wat wel goed vertaalt naar een sprite"**. Dus alle vier: snavel; verhoudingen (kop/lijf/bolletje zoals foto 5); vleugels (lange gevouwen vleugels die achter/onder over het korte staartje kruisen, foto 6/7); dons/veren (pluizig dons, gespikkelde keel/borst, foto 1/5), alleen in een vorm die op 64×64 leest.
  - Snavel: **"Langer en dun, dicht"** (zoals het uitvliegertje op foto 1/5). Dit vervangt het korte open bedelbekje van 2–5 nov.
  - Kleuren: **"Ja, kleuren blijven"** (mild lila/grijsviolet, lichte donzige buik, Starly-oog zonder iris, geen blauwgroen, oranje pootjes).
  - Pose: **"Bolletje zoals foto 5"** (ineengedoken uitvliegertje, `../referenties/jordi_5_uitvlieger_hand.webp`).

## Bijlagen
1. `bijlage1_foto5_uitvlieger.png`: foto 5, bijgesneden rond het vogeltje en **gespiegeld** (kop links, zodat de 3/4 naar links klopt). Anatomie en pose.
2. `bijlage2_huidige_sprite_8x.png`: huidige sprite, alleen voor de kleuren ("do not trace").

Nieuw gesprek per poging; niet lang bijsturen (Gemini drijft af).

## Prompt v1

```
Design a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), drawn fresh as a Game Freak artist would.

THE CREATURE
- A baby hummingbird Pokémon: a hummingbird chick, a fledgling that has just left the nest. It must read clearly as a hummingbird chick, not as a sparrow, finch or generic songbird.
- Attachment 1 is a photo of a real hummingbird fledgling sitting in a hand. Use it for the anatomy and the pose: a small hunched round ball of a bird, head sunk into the body, wings folded along the sides. Copy the bird's pose and proportions from the photo (not the hand).
- Beak: a long, thin, straight hummingbird beak, CLOSED, like in the photo. Dark beak.
- Proportions: like the fledgling in the photo, a round little ball with the head sunk into the shoulders, no neck.
- Wings: long folded hummingbird wings lying along the sides, their tips sticking out behind/below the body and crossing over the short tail.
- Down: fluffy downy plumage with a speckled throat and chest, as in the photo, but ONLY in a way that still reads in a 64x64 sprite: a few clear fluffy tufts in the outline and a few clear speckle pixels, no fine fur texture or noise that disappears at sprite size.
- Exactly one head, two folded wings, one short tail, two tiny feet.

COLORS (keep these exactly)
- Attachment 2 is the old sprite of this Pokémon. Use it ONLY for the colors. Do NOT trace it or copy its shape or pose.
- Soft mild lilac / grey-violet plumage, a pale fluffy lavender-white belly, darker blue-violet folded wings, small orange feet, a small yellow mouth corner at the base of the beak.
- Eye: a clear, defined black eye with a white highlight (like Starly's eye), no colored iris.
- No teal, green or blue-green anywhere. Gentle and friendly, not mysterious or dark.

POSE AND VIEW
- 3/4 view facing left, head turned towards the viewer, like official Gen 3 bird sprites (Taillow, Starly).
- Compact, fits in a square.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites, large calm shading areas, no noise.
- Plain white background. No hand, no branch, no nest, no ground, rock, shadow or base.
- No sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Taillow, Starly, Pidgey, Natu or Fletchling. Not a sparrow or a chick from a hen.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```

## Ronde 1 (Jordi, 19 nov, letterlijk): `r1_beter.png`
"beter, maar de kleuren zijn niet meer hetzelfde en hij kijkt niet genoeg diagonaal naar boven zoals in de foto"

## Bijsturing r1 → r2 (zelfde gesprek; werkt hooguit 1–2 keer)

```
Better! Keep this design, pose, body shape, wings, beak shape, speckles and feet exactly as they are. Change only two things:
1. COLORS: the colors drifted to plain grey. Use the exact colors of attachment 2 (the old sprite): lilac / grey-violet plumage (main tone #9686C8, light #BAB0E0, shadow #6C5A9C), pale lavender-white belly (#E0DCF4), darker blue-violet folded wings (#605AAA and #3E3480), orange feet (#E29628), dark outline (#140E1E). Clearly violet, not grey.
2. HEAD ANGLE: like the fledgling in attachment 1, the head is tilted so the bird looks diagonally UP: the beak points diagonally up to the upper left (about 30 degrees above horizontal), not straight forward. The body stays the same round ball.
```

## Ronde 2 (Jordi, 19 nov, letterlijk): `r2_goed.png`
"ok dat is ook goed, is de pose driekwart genoeg denk je?"

## Ronde 3 (Jordi, 19 nov, letterlijk): `r3_zelfde.png` (na bijsturing kopdraai)
"dit is precies hetzelfde toch? dus nieuw gesprek lijkt me"

## Prompt v2 (nieuw gesprek)
Bijlagen: `bijlage1_foto5_uitvlieger.png`, `bijlage2_huidige_sprite_8x.png`, `bijlage3_kophoek_taillow_starly.png` (alleen voor de kophoek). r2 niet als bijlage (Gemini kopieert een bijlage + "keep" letterlijk); in plaats daarvan staan de r2-correcties (kleurcodes, kop omhoog) in de tekst.

```
Design a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), drawn fresh as a Game Freak artist would.

THE CREATURE
- A baby hummingbird Pokémon: a hummingbird chick, a fledgling that has just left the nest. It must read clearly as a hummingbird chick, not as a sparrow, finch or generic songbird.
- Attachment 1 is a photo of a real hummingbird fledgling sitting in a hand. Use it for the anatomy: a small hunched round ball of a bird, head sunk into the body, no neck, wings folded along the sides.
- Beak: a long, thin, straight hummingbird beak, CLOSED. Dark beak.
- Wings: long folded hummingbird wings lying along the sides, their tips sticking out behind/below the body and crossing over the short tail.
- Down: fluffy downy plumage with a speckled throat and chest, but ONLY in a way that still reads in a 64x64 sprite: a few clear fluffy tufts in the outline and a few clear speckle pixels, no fine texture or noise.
- Exactly one head, two folded wings, one short tail, two tiny feet.

POSE AND VIEW (most important)
- Body in 3/4 view facing left: belly towards the viewer, near wing along the side.
- The HEAD is turned MORE towards the viewer than the body, exactly like the heads of Taillow and Starly in attachment 3: we see the face partly from the front, the eye sits on the front-side of the head, and a hint of the far side of the face is visible. NOT a flat side-profile head.
- The bird looks diagonally UP: the beak points diagonally up to the upper left, about 30 degrees above horizontal.
- The far foot is placed a bit higher and further back than the near foot.
- Compact, fits in a square.

COLORS (keep these exactly)
- Attachment 2 is the old sprite of this Pokémon. Use it ONLY for the colors. Do NOT trace it or copy its shape or pose.
- Lilac / grey-violet plumage (main tone #9686C8, light #BAB0E0, shadow #6C5A9C), pale lavender-white belly (#E0DCF4), darker blue-violet folded wings (#605AAA and #3E3480), orange feet (#E29628), dark outline (#140E1E), a small yellow mouth corner at the base of the beak. Clearly violet, not grey.
- Eye: a clear, defined black eye with a white highlight (like Starly's eye), no colored iris.
- No teal, green or blue-green anywhere. Gentle and friendly, not mysterious or dark.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites, large calm shading areas, no noise.
- Plain white background. No hand, no branch, no nest, no ground, rock, shadow or base.
- No sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Attachment 3 is ONLY for the head angle: do not copy Taillow's or Starly's design, colors, crest or beak.
- Not Taillow, Starly, Pidgey, Natu or Fletchling. Not a sparrow or a chick from a hen.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```
