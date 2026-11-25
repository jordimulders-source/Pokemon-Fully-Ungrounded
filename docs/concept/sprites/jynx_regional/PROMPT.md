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
