# Gemini-prompt: Picaraio opknappen (19 nov)

Opknapronde: `../../OPKNAPRONDE_GEMINI.md`. Regels: `docs/lessen/GEMINI.md`.

## Jordi (19 nov, letterlijk)
"Picaraio mag iets meer de gen 1 Raichu pose, en de krullen bovenop het hoofd mogen iets natuurlijker naar beneden golven. Kleuren en staart verder prima, hoofd is een beetje knullig, snavel mag iets meer fearow achtig." · "Picaraio ziet er nog een beetje klunzig uit"

## Bijlagen
1. `bijlage1_huidige_sprite_8x.png` (huidige sprite: design, kleuren, staart)
2. `bijlage2_raichu_gen1_8x.png` (Gen 1 Raichu, Jordi's inspiratie voor de pose)
Fearow alleen in woorden (keuze Claude: een sprite van een bestaande Pokémon als bijlage wordt vaak gekopieerd).

## Prompt v1 (nieuw gesprek)
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left in 3/4 view.

ATTACHMENTS
- Attachment 1 is the current sprite. It looks a bit clumsy. Use it for the design, the colors and the tail, which are all good and must stay. Do NOT trace its pose or its head: those must improve.
- Attachment 2 is the Gen 1 Raichu sprite. Use it ONLY as inspiration for the pose: move the pose a bit more towards this one (hunched forward, crouching and tense, big round head, round belly, the tail swinging in a big arc around and under the body, filling the frame). Do not copy Raichu's body, ears or face; it stays a bird.

THE CREATURE (keep)
- Electric/Flying, the evolution of a Pikachu-like woodpecker; it relates to its pre-evolution like Raichu to Pikachu. Based on the chestnut woodpecker (Celeus elegans).
- Big, imposing, puffed-up bird. Chestnut / orange-brown body, large cream belly, small red cheek patch, grey beak and grey feet.
- Wings half open, chestnut with round cream spots (no scale pattern).
- Tail: exactly as in attachment 1: a thin black cord in a loop that ends in a big yellow zigzag lightning bolt.
- On top of the head: thin black feather strands that end in curls (inspired by Raichu's ears).

WHAT MUST CHANGE
- Pose: a bit more like the Gen 1 Raichu pose (see above). Exactly two wings, two legs, one tail.
- Head: the head looks clumsy now. Make it a well-shaped, round bird head that belongs to an official Pokémon, turned towards the viewer in 3/4, one clear eye, the red cheek below and behind the eye.
- Beak: more like Fearow's beak: long, sharp and pointed, slightly hooked at the tip, grey. Still a woodpecker beak, not red.
- Head curls: the black feather strands on top of the head should wave down more naturally, flowing backwards and downwards from the crown like real feathers, ending in curls. Not standing straight up.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No branch, ground, rock, shadow or base. No sparkles or effects except the lightning bolt at the end of the tail. One single creature.

AVOID
- Not Raichu, Fearow, Pidgeot, Spearow or Woody Woodpecker. No plush toy, chibi or mascot look, no oversized sparkly eyes.
```

## Ronde 1 (prompt v1) → `r1_prompt_v1.png`
Jordi (19 nov): "het oog is niet goed, de snavel is toch wat te dik, die mag wat dunner, en hij heeft niet de juiste pose, plus hij is wat te dik, de hoofdkrullen zijn ook nog niet echt natuurlijk en de staart is een lus ipv een staart"
→ te veel punten voor bijsturen: nieuw gesprek, zelfde bijlagen, prompt v2.

## Prompt v2 (nieuw gesprek; bijlagen 1 en 2)
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left in 3/4 view.

ATTACHMENTS
- Attachment 1 is the old, clumsy sprite of this Pokémon. Use it ONLY for the colors and the design idea. Do NOT trace its pose, head, body shape or tail.
- Attachment 2 is the Gen 1 Raichu sprite. Copy its POSE and ATTITUDE onto the bird (not its body, ears or face): the body leans forward and is hunched, the head is low and pushed forward, the legs are bent as if ready to pounce, tense and aggressive, filling the frame. The tail starts at the back of the body and swings in a big S-curve behind and under the body, ending in the lightning bolt at the bottom left.

THE CREATURE
- Electric/Flying, the evolution of a Pikachu-like woodpecker (like Raichu to Pikachu). Based on the chestnut woodpecker (Celeus elegans).
- Colors: chestnut / orange-brown body, cream belly, small red cheek patch, grey beak and feet, wings chestnut with round cream spots.
- Body: strong and imposing but NOT fat or round like a ball. A sleek, muscular bird body; the cream belly is an oval on the chest, not a huge ball.
- Wings half open. Exactly two wings, two legs, one tail.
- Eye: a round black eye with one small white shine pixel, like its pre-evolution. No eyelid, no white sclera, no human-like eye, not sad.
- Beak: long, thin, sharp and pointed like Fearow's beak, slightly hooked at the tip, grey. Thin, not thick.
- Head plumes: two or three thin black feather plumes that grow from the back of the crown, sweep backwards and droop down in a natural soft curve, each ending in a small curl. Like real crest feathers, not wires or antennas.
- Tail: a REAL tail, not a ring or a loop around the body. A thin black tail that grows from the rump and swings in one S-curve, ending in a big yellow zigzag lightning bolt.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No branch, ground, rock, shadow or base. No effects except the lightning bolt at the end of the tail. One single creature.

AVOID
- Not Raichu, Fearow, Pidgeot, Spearow, a kiwi or Woody Woodpecker. No plush toy, chibi or mascot look.
```

## Ronde 2 (prompt v2) → `r2_prompt_v2.png`
Jordi (19 nov): "schrap de fearow snavel, hij maakt er ook meteen een fearow hoofd van en dat wil ik niet, plus fearow pose, alle mentions naar fearow moeten eruit"
→ Fearow vervalt overal (ook in AVOID). Snavel: de spechtensnavel uit bijlage 1, wat dunner (Jordi r1: "te dik, die mag wat dunner").

Jordi (19 nov): "de krullen zijn wel eindelijk goed" (r2) → kuifregel in v3 beschrijft de krullen van r2 (r2 zelf niet als bijlage: dan komt de Fearow-kop mee).

## Prompt v3 (nieuw gesprek; bijlagen 1 en 2)
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left in 3/4 view.

ATTACHMENTS
- Attachment 1 is the old, clumsy sprite of this Pokémon. Use it ONLY for the colors and the design idea. Do NOT trace its pose, head, body shape or tail.
- Attachment 2 is the Gen 1 Raichu sprite. Copy its POSE and ATTITUDE onto the bird (not its body, ears or face): standing on the ground, the body leans forward and is hunched, the head is low and pushed forward, the legs are bent as if ready to pounce, tense and aggressive, filling the frame. The tail starts at the back of the body and swings in a big S-curve behind and under the body, ending in the lightning bolt at the bottom left. It is NOT flying.

THE CREATURE
- Electric/Flying, the evolution of a Pikachu-like woodpecker (like Raichu to Pikachu). Based on the chestnut woodpecker (Celeus elegans).
- Colors: chestnut / orange-brown body, cream belly, small red cheek patch, grey beak and feet, wings chestnut with round cream spots.
- Body: strong and imposing but NOT fat or round like a ball. A sleek bird body; the cream belly is an oval on the chest.
- Wings half open. Exactly two wings, two legs, one tail.
- Head: a round woodpecker head. No big feather crest on the head, only the thin black plumes described below.
- Eye: a round black eye with one small white shine pixel, like its pre-evolution. No eyelid, no white sclera, no human-like eye, not sad.
- Beak: the grey woodpecker chisel beak from attachment 1, but a bit thinner.
- Head plumes: two thin black strands that start at the forehead, run back over the top of the head in one long smooth arch, and hang down behind the head, each ending in a small curl. Thin like hairs, close to the head.
- Tail: a REAL tail, not a ring or a loop around the body. A thin black tail that grows from the rump and swings in one S-curve, ending in a big yellow zigzag lightning bolt.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No branch, ground, rock, shadow or base. No effects except the lightning bolt at the end of the tail. One single creature.

AVOID
- Not Raichu, Pidgeot, Spearow, a kiwi, a hoopoe or Woody Woodpecker. No plush toy, chibi or mascot look.
```

## Ronde 3 (prompt v3) (plaatje niet als bestand ontvangen)
Beschrijving Claude: kleiner, slank lijf, vleugel half open, kop met een extra oortje/tuft links, krullen boven de kop, staart als grote boog naar de bliksem linksonder, wang weg.
Jordi (19 nov): "ik vind hem nu teveel van het origineel afwijken, te klein ogend"
Oorzaak (Claude): v2/v3 zeiden "old, clumsy sprite, ONLY for colors" en "NOT fat ... sleek"; dat duwde hem van het origineel weg (origineel: "imposant, groot, opgeblazen").

## Prompt v4 (nieuw gesprek; bijlagen 1 en 2)
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left in 3/4 view.

ATTACHMENTS
- Attachment 1 is the current sprite. It is the BASE: keep its size, its big imposing puffed-up body, its proportions, its colors, its wings with round cream spots, its red cheek and its overall look. It should look like the same Pokémon, only better drawn. Only the few points under "WHAT CHANGES" are different.
- Attachment 2 is the Gen 1 Raichu sprite: inspiration for the pose only (leaning forward, tense, tail swinging in a big curve under the body, filling the frame). Do not copy Raichu's body, ears or face.

WHAT CHANGES (only this, and only a little)
1. Pose: a bit more like the Gen 1 Raichu pose: leaning a bit more forward and tense. Still standing, not flying.
2. Head: the head looks a bit clumsy. Make it a nicer round bird head, still the same size and colors, with a round black eye with one white shine pixel and the red cheek below and behind the eye. No extra ears or tufts.
3. Beak: the same grey woodpecker beak, but a bit thinner.
4. Head plumes: two thin black strands that start at the forehead, run back over the top of the head in one long smooth arch and hang down behind the head, each ending in a small curl. Thin like hairs, close to the head.
5. Tail: a real tail, not a loop: the thin black tail grows from the rump and swings in a curve under the body, ending in the big yellow zigzag lightning bolt.

KEEP
- Big and imposing; the sprite fills most of the 64x64 frame, like a final evolution. Not smaller or slimmer than attachment 1.
- Exactly two wings, two legs, one tail.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, shadow or base. No effects except the lightning bolt. One single creature.

AVOID
- Not Raichu, Pidgeot or Spearow. No plush toy, chibi or mascot look.
```

## Ronde 4 (prompt v4) → `r4_prompt_v4.png`
Jordi (19 nov): "hij is prima, alleen te dik, daardoor wordt zijn vleugel ook zo wimpy. En ik wil meer een vliegende achteroverleunende pose zoals het origineel."

### Verbeterprompt r5 (in hetzelfde gesprek)
```
Good, keep the head, beak, eye, cheek, head plumes, colors, the tail with the lightning bolt and the style exactly as they are. Change only two things:

1. Body: a bit less fat. Slimmer belly and chest, so the body is less of a ball. Still a strong bird.
2. Pose: a flying pose leaning backwards, like attachment 1: the body tilted back, chest forward and up, head up, in the air, legs hanging below the body. The near wing is raised high and spread wide, big and powerful with clear long flight feathers (not a small wimpy wing). The far wing is partly visible behind the body. Exactly two wings, two legs, one tail.

Same 64x64 Gen 3 sprite, white background, nothing else changed.
```

## Ronde 5 (verbeterprompt r5)
Jordi (19 nov): "ok prima, alleen de pose is niet achteroverleunend en er is een extra donderschok bij gekomen"

### Verbeterprompt r6 (in hetzelfde gesprek)
```
Good. Change only these three things, keep everything else exactly:

1. Remove the extra small lightning bolt next to the tail. There is only ONE lightning bolt: the big one at the end of the tail.
2. Lean the whole bird backwards: tilt the body about 30 degrees back, so the head and shoulders are further to the right and higher, and the chest and belly face up and to the left, like a bird braking in the air just before landing. The legs hang forward under the belly. Head, tail and colors stay as they are. Exactly two wings, two legs, one tail.
3. The wing pattern is gone. Bring it back as in the previous version: the wings are chestnut / orange-brown (not cream) with round cream spots on them.

Same 64x64 Gen 3 sprite, white background.
```

Jordi (19 nov): "en het vleugelpatroon is verdwenen" → punt 3 in r6.

## Ronde 6 (verbeterprompt r6): afgedreven
Jordi (19 nov): "hij snapt het weer niet" (gespiegeld naar rechts, staart weg, vleugel nog crème, kuif weg).
→ nieuw gesprek. Pose = die van het origineel (Jordi: "vliegende achteroverleunende pose zoals het origineel"), dus de Raichu-bijlage vervalt.

## Prompt v5 (nieuw gesprek; alleen bijlage 1)
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing LEFT in 3/4 view.

ATTACHMENT
- The attachment is the current sprite. It is the BASE: keep its pose (flying, leaning backwards, chest forward and up, the near wing raised and spread, legs hanging), its size (big and imposing, filling most of the frame), its colors, its red cheek and its overall look. It should look like the same Pokémon, only better drawn. Only the points under "WHAT CHANGES" are different.

WHAT CHANGES (only this)
1. Body: slim it a little. Strong and imposing, but not a round ball.
2. Wing: the near wing big and powerful, with long clear flight feathers. Chestnut / orange-brown with round cream spots, like the attachment. Not cream, no stripes.
3. Head: a nicer round bird head, same size and colors, a round black eye with one white shine pixel, the red cheek below and behind the eye. No extra ears or tufts.
4. Beak: the same grey woodpecker beak, a bit thinner.
5. Head plumes: two thin black strands that start at the forehead, run back over the top of the head in one long smooth arch and hang down behind the head, each ending in a small curl. Thin like hairs.
6. Tail: a real tail, not a loop: a thin black tail that grows from the rump and swings in one curve below the body, ending in ONE big yellow zigzag lightning bolt. No other lightning bolts.

Exactly two wings, two legs, one tail.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, shadow or base. No effects except the one lightning bolt. One single creature.

AVOID
- Not Pidgeot, Spearow or a sparrow. No plush toy, chibi or mascot look.
```

## Ronde 7 (prompt v5) → `r7_prompt_v5_illustratie.png`
Jordi (19 nov): "uitstekend, maar het is geen sprite"

### Verbeterprompt r8 (in hetzelfde gesprek)
```
Excellent, this is exactly the design. Now convert THIS image into pixel art: an official Gen 3 front sprite (Ruby/Sapphire/Emerald), 64x64 pixels, max 16 colors, 1 px dark outline, light from top left, clean Game Freak shading.
Do not change anything about the design: same pose, same angle, same proportions, same head, beak, eye, cheek, head plumes, wings with spots, legs, tail and lightning bolt, same colors. Only the drawing style changes, from illustration to sprite. White background.
```

## Ronde 8 → `r8_fijn_gepixeld.png`
Gemini pixelde alleen fijn over de illustratie (geen 64×64-raster). Jordi (19 nov): "hij snapt het niet? Met deze afbeelding nog een nieuw gesprek proberen?"

## Prompt v6 (nieuw gesprek; enige bijlage: `bijlage_ontwerp_r7.png`)
```
The attachment is the official concept art of a Pokémon. Draw its in-game front sprite, exactly as Game Freak would for Pokémon Ruby/Sapphire/Emerald.

- The design is final: same pose, angle, proportions, head, beak, eye, red cheek, the two thin black head plumes with a curl, wings with cream spots, legs, the thin black tail and the lightning bolt, same colors. Do not add, remove or change anything.
- Real low-resolution pixel art: the whole sprite is a 64x64 pixel grid. Show it enlarged with big, clearly visible square pixels (each sprite pixel is one big block), not a smooth or finely pixelated illustration.
- Max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 2-3 tones per color, no gradients, no anti-aliasing, no noise.
- Thin parts (head plumes, tail) become 1 px lines.
- Plain white background, one single creature, no effects besides the lightning bolt.
```

## Sprite v2 (19 nov)
- r4, Jordi: "nice, model staat, je mag nu wel kleur en schaduw bijwerken nog in de keuring ronde" → vorm r4 bevroren; kleurronde in sprite_v2/kleur/.
- Jordi: "vooral de staartdonderschok" (kleurronde).
