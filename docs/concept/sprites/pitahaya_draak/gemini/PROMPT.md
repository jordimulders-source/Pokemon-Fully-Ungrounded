# Gemini-prompt: pitahaya-draak fase 1, startprompt v1 (16 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn en besluiten: `docs/concept/IDEEEN.md` (Pseudo-legendary draak: pitahaya).
Bijlage: zelf toevoegen (Jordi): een foto van een roze pitahaya (heel, met schubben) en een foto van de cactusrank (groene driekantige stengel).

## Jordi (letterlijk, 16 nov)
- "tijd voor de dragonfruit dragon lijn, 3 fases. 1e is een dragonfruit hoofd met een lichaam eronder"
- "de roze met witte binnenkant" / "dan doen we die"
- "een slang zou ik saai vinden voor deze vorm, we kunnen wel anders meer de komodo draak kant op gaan"
- "dan is fase 2 een teju en fase 3 mag op 2 poten staan, maar voorover leunend, komodo draak"

## Keuzes Claude (schrappen mag)
- De groene schubpunten van de schil als stekels/kuif.

## Jordi (16 nov), reactie op v1
- "hij moet niet een kleine hagedis zijn. Het gezicht zit in de vrucht bij fase 1, maar daarna komen er meer kenmerken bij"
- Lichaam: "b, een stukje cactusrank als lijf" (keuze uit: a knolachtig lijfje, b cactusrank, c alleen pootjes).

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The first stage of a three-stage dragon line (pseudo-legendary). Stage 2 will be a tegu lizard, stage 3 a Komodo-dragon-like dragon leaning forward on two legs.
- Stage 1: its head IS a pink dragon fruit (pitahaya: hot pink skin with green-tipped scales), with a small body underneath.
- The body is a short piece of the pitahaya cactus stem: green, three-ribbed (triangular cross-section) with wavy edges and tiny areoles along the ribs, like the real climbing cactus the fruit grows on.
- Use the attached photos for the fruit and the stem: pink skin, the shape and placement of the scale flaps with green tips.

DESIGN
- The fruit head is large compared to the body (about half of the creature or more). The face is in the fruit.
- Colors: hot pink head, green scale tips, green stem body. Keep it simple.
- Readable silhouette: big round-oval fruit head with scale flaps sticking out, short cactus-stem body below.

POSE
- Three-quarter view facing left, curious.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature smaller than the canvas (it is a first stage), max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO floor, shadow, base platform, leaves, glow or effects. One single creature, no extra views.

AVOID
- Not a lizard, no lizard body. Not a lizard holding or wearing a separate fruit: the fruit IS its head.
- Not a snake. No wings.
- Not Applin-like (no fruit with a creature peeking out of it). Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

---

# Prompt v2 (16 nov): zelfde gesprek, reactie op r1 (`r1.png`)

## Jordi (letterlijk)
- "het gezicht is stom en niet passend, de armen en benen mogen iets substantieler, het idee klopt wel goed"

```
The idea is right, keep the fruit head and the cactus-stem body exactly as they are. Change only two things:

1. The face: replace it completely. The current face is silly and doesn't fit a Pokémon that will evolve into a tegu lizard and then a Komodo dragon. Remove the blush marks, the dot nostrils and the small smile.
2. The arms and legs: make them a bit more substantial (thicker and sturdier), still made of the same green cactus stem.

Same pose, same colors, same Gen 3 sprite style, plain white background.
```

---

# Prompt v3 (16 nov): zelfde gesprek, reactie op r2 (`r2.png`)

## Jordi (letterlijk)
- "beter, het gezicht moet wel nog beter [...] Hij is namelijk wel grass nu, maar nog niet echt dragon"

## Keuzes Claude (schrappen mag): reptielenogen met spleetpupil, wenkbrauwrand als schubben, brede bek met een klein tandje.

```
Much better, keep everything except the face. The body, arms, legs, fruit head and pose are good now.

The face still reads only as a plant. It must also read as a young DRAGON (the first stage of a dragon line):
- Reptile eyes: yellow or amber with a vertical slit pupil, set under a heavy scaly brow ridge.
- A wide lizard mouth across the fruit instead of the small human frown, with one small fang showing.
- No human nose. No eyebrows drawn as lines.
The face is still part of the fruit skin, not a separate mask.

Same pose, same colors, same Gen 3 sprite style, plain white background.
```

---

# Prompt v4 (16 nov): zelfde gesprek, reactie op r3 (`r3.png`)

## Jordi (letterlijk)
- "het is wat beter, maar gelijk wel wat overdreven, het moet een fase 1 dragon zijn, een gible, axew achtig"

```
Better, but the face is now too much. It must be a first-stage baby dragon, like Gible or Axew: simple, young and a bit innocent, with only a hint of dragon.
- Tone the face down to the level of Gible and Axew: big simple eyes (keep the amber color), less heavy brow, fewer scale bumps on the forehead.
- Simpler mouth, like Gible's or Axew's; at most one tiny fang, or none.
Keep everything else exactly as it is: fruit head, cactus-stem body, arms, legs, pose, colors, Gen 3 sprite style, plain white background.
```

---

# Prompt v5 (16 nov): zelfde gesprek, reactie op r4 (`r4.png`)

## Jordi (letterlijk)
- "ok ik vind de ogen nu teveel neopets, de rest is goed"

```
Very good, keep EVERYTHING exactly as it is, only change the eyes.
The eyes are now too big, glossy and cartoon-mascot-like (Neopets style). Make them like the eyes of official Gen 3 Pokémon sprites such as Gible or Bagon: smaller and simpler, a flat amber/yellow iris with a dark pupil and one single small white highlight pixel, a clear dark outline around the eye. No big shiny anime pupils, no multiple highlights, no eyelashes.
Same face otherwise (mouth, small fang, snout), same pose, colors, Gen 3 sprite style, plain white background.
```

---

# r5 (16 nov, `r5.png`): Jordi: "wederom beter, alleen nog niet de juiste blik in de ogen". Welke blik: gevraagd.
- Jordi koos **c, brutaal en ondeugend** (uit: a dapper/vastberaden, b nieuwsgierig/alert, c brutaal/ondeugend).

# Prompt v6 (16 nov): zelfde gesprek

```
Great, keep EVERYTHING exactly as it is, only change the expression of the eyes.
The eyes look empty now and don't focus on anything. Give them a cheeky, mischievous, slightly provoking look, like a little troublemaker challenging the opponent: a clear dark pupil looking straight at the opponent (to the left), upper eyelid slightly lowered for a sly, cocky look. Keep it a young baby dragon (Gible/Axew level), not angry or evil.
Keep the eye size, the amber color, the simple Gen 3 style eyes, the mouth with the small fang, pose, colors and plain white background.
```
