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
