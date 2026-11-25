# Regionale Jynx (sirene) – Gemini-prompt v1 (25 nov)

Besluiten Jordi: vogelvrouw zoals in de Odyssee; Fairy/Dark; kleuren voorstel 1 (vaas: vogelhelft terracotta met zwarte tekening, gezicht wit zoals vrouwen op vazen); gezicht qua vorm van Jynx; haar en lippen een andere kleur dan Jynx; "haren bruin"; haarstijl mag passender bij een sirene.

Eigen invulling Claude (niet door Jordi gekozen, schrappen/aanpassen mag): lippen purperrood, lange golvende lokken, pose zingend op vogelpoten met half gespreide vleugels, menselijke armen weggelaten (vogellijf met vrouwenhoofd zoals op de vazen).

## Prompt (Engels, zonder bijlage)

```
Design an original Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, white background, no ground, no shadow, no effects, no glow, no music notes.

WHAT IT IS: a siren from Homer's Odyssey, exactly as painted on ancient Greek vases: the body of a large bird with the head of a woman. Fairy/Dark type: beautiful, but it lures sailors to their death with its song.

POSE (most important): standing upright on two bird legs with talons, seen in 3/4 view facing left (the far wing on the left, partly hidden; the near wing on the right). Both wings half spread. Head raised, mouth open in song. Compact, fits in a square, wings close to the body. Exactly two wings, two legs, no human arms.

FACE: wide, rounded face; very large, full, puffy lips that take up most of the lower half of the face; small, narrow, heavy-lidded eyes; no visible nose. Describe it with this shape only.

HAIR: brown, long and wavy, falling in locks over the shoulders and onto the wings.

COLORS (ancient Greek vase painting): the bird body and feathers in terracotta orange with black lines and black feather patterns, like black-figure pottery. The face is white, the way women's skin was painted on Greek vases. Lips deep purple-red. Hair brown.

DO NOT: plush or Neopets style, a mermaid or fish tail, a human body with wings (angel or harpy), a crown, jewellery, a lyre or other objects, starfield or galaxy patterns, a Greek meander border, realistic painting.
```

## r1 (25 nov): afgekeurd
`gemini/r1.png`. Jordi: "echt vreselijk, lijkt totaal niet op jynx, gewoon een vogel met een mensenhoofd". Oorzaak: prompt vroeg letterlijk een vogellijf met vrouwenhoofd en beschreef Jynx' bouw niet; Gemini gaf er ook een snavel bij.

# Prompt v2 (25 nov): Jynx-bouw als basis, sirene erin
Bijlage: `gemini/bijlage_jynx_gen3.png` (bovenste frame).
Eigen invulling Claude (niet door Jordi gekozen): armen worden vleugels, jurk wordt verenkleed, vogelklauwen onder de jurk; lippen purperrood; haar lang golvend.

```
The attached image is JYNX, a Gen 3 Pokémon sprite. Design a REGIONAL FORM of Jynx: it must still be instantly recognizable as Jynx, but clearly different. Its theme: a siren from Homer's Odyssey (half woman, half bird, luring sailors with its song). Fairy/Dark type.

Output: an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, white background, no ground, no shadow, no effects, no music notes.

KEEP FROM JYNX (most important): the overall silhouette and proportions: the big head with the same face shape (wide face, huge full lips, small heavy-lidded eyes, no nose), hair falling down both sides of the body like a cape, the wide bell-shaped dress body that hides the legs, both arms raised in the same pose. Same front-facing view as the attachment.

CHANGE INTO A SIREN:
- The two raised arms are bird wings (exactly two wings, no extra arms).
- The dress is made of feathers, like a bird's plumage.
- Two bird feet with talons peek out under the feathered dress.
- No beak: the face stays Jynx's face.
- Hair: brown, long and wavy.

COLORS (ancient Greek black-figure vase painting): feathers terracotta orange with black lines and black feather patterns; face white, the way women's skin was painted on Greek vases; lips deep purple-red; hair brown. No purple skin, no golden hair, no pink lips, no red dress.

DO NOT: a realistic bird with a human head, a beak, a mermaid tail, an angel, jewellery, a crown, a lyre, plush style.
```

## r2 (25 nov, prompt v2)
`gemini/r2.webp`. Jordi: "beter maar het is geen sprite, herken je er genoeg sirene in? hij heeft teveel detail ook".
Claude stelde voor: 1 zingend + lokkende blik, 2 onderlijf meer vogel (staartveren), 3 borstmotief weg en rustig verenkleed, 4 weinig detail. Jordi: "2 mee oneens, dan gaat gemini een vogel met een mensenhoofd bouwen. voor de rest akkoord".

# Prompt v3 (25 nov) = v2 + punten 1, 3, 4 (nieuw gesprek, bijlage `gemini/bijlage_jynx_gen3.png`)

```
The attached image is JYNX, a Gen 3 Pokémon sprite. Design a REGIONAL FORM of Jynx: it must still be instantly recognizable as Jynx, but clearly different. Its theme: a siren from Homer's Odyssey (half woman, half bird, luring sailors with its song). Fairy/Dark type.

Output: a simple, clean official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, flat colors with 2-3 shades per color, few lines, the same low level of detail as the attached Jynx. White background, no ground, no shadow, no effects, no music notes.

KEEP FROM JYNX (most important): the overall silhouette and proportions: the big head with the same face shape (wide face, huge full lips, small heavy-lidded eyes, no nose), hair falling down both sides of the body like a cape, the wide bell-shaped dress body that hides the legs, both arms raised in the same pose. Same front-facing view as the attachment.

CHANGE INTO A SIREN:
- It is singing: mouth open in song, with an alluring, tempting look in its eyes (not bored).
- The two raised arms are bird wings (exactly two wings, no extra arms).
- The dress is made of feathers, like a bird's plumage: calm, large areas of color with only a few black lines, like a Greek vase painting. No pattern or round shapes on the chest.
- Two bird feet with talons peek out under the feathered dress.
- No beak: the face stays Jynx's face.
- Hair: brown, long and wavy.

COLORS (ancient Greek black-figure vase painting): feathers terracotta orange with black lines; face white, the way women's skin was painted on Greek vases; lips deep purple-red; hair brown. No purple skin, no golden hair, no pink lips, no red dress.

DO NOT: a realistic bird with a human head, a beak, a mermaid tail, an angel, jewellery, a crown, a lyre, plush style, detailed individual feathers.
```

## r3 (25 nov, prompt v3)
`gemini/r3.webp`. Jordi: "verwijzen naar de vaas stijl zorgt voor deze vormen, je moet de kleuren beschrijven met kleurcodes en verder niet naar de vaas verwijzen".

# Prompt v4 (25 nov) = v3 zonder elke vaasverwijzing, kleuren als hexcodes (tinten gekozen door Claude)

```
The attached image is JYNX, a Gen 3 Pokémon sprite. Design a REGIONAL FORM of Jynx: it must still be instantly recognizable as Jynx, but clearly different. Its theme: a siren from Homer's Odyssey (half woman, half bird, luring sailors with its song). Fairy/Dark type.

Output: a simple, clean official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, flat colors with 2-3 shades per color, few lines, the same low level of detail as the attached Jynx. White background, no ground, no shadow, no effects, no music notes.

KEEP FROM JYNX (most important): the overall silhouette and proportions: the big head with the same face shape (wide face, huge full lips, small heavy-lidded eyes, no nose), hair falling down both sides of the body like a cape, the wide bell-shaped dress body that hides the legs, both arms raised in the same pose. Same front-facing view as the attachment.

CHANGE INTO A SIREN:
- It is singing: mouth open in song, with an alluring, tempting look in its eyes (not bored).
- The two raised arms are bird wings (exactly two wings, no extra arms).
- The dress is made of feathers, like a bird's plumage: calm, large areas of color with only a few lines. No pattern or round shapes on the chest.
- Two bird feet with talons peek out under the feathered dress.
- No beak: the face stays Jynx's face.
- Hair: long and wavy.

COLORS (exact hex codes):
- Feathers: #E07A3C (light), #C4612A (base), #8E3F1A (shadow)
- Face: #FFFFFF (light), #E8E2DA (shadow)
- Lips: #8E2A4A (base), #5E1A30 (shadow)
- Hair: #8A5A34 (light), #6B4226 (base), #45291A (shadow)
- Outline: #1A1210
No purple skin, no golden hair, no pink lips, no red dress.

DO NOT: a realistic bird with a human head, a beak, a mermaid tail, an angel, jewellery, a crown, a lyre, plush style, detailed individual feathers.
```

## r4 (25 nov, prompt v4)
`gemini/r4.png`. Jordi: "het design is ok, ze lijkt te slaperig, verder is het geen driekwart".

# Prompt v5 (25 nov): nieuw gesprek, alleen r4 als bijlage (GEMINI.md: eigen design + "same pose, only angle"), 2 wijzigingen

```
The attached image is my Pokémon design. Keep the design exactly the same: same head, face shape, lips, brown hair, feathered dress, wings, talons, same colors, same simple Gen 3 sprite style and level of detail (64x64, max 16 colors, white background, no shadow, no effects).

Change ONLY these two things:
1. VIEW: turn it to a 3/4 view facing left, like most Gen 3 front sprites. The far side (its left wing, left side of the hair) is on the left of the image, partly hidden behind the body and drawn smaller; the near side (its right wing) is on the right, larger. The face is turned toward the left, both eyes still visible, the far eye slightly narrower.
2. EYES: less sleepy. The eyes are more open, with an alluring, tempting gaze, as if luring you in with its song. Mouth stays open, singing.

Exactly two wings, two feet, no beak, no extra arms.
```
