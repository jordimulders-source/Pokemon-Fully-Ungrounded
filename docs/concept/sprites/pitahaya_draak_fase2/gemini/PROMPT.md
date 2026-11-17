# Gemini-prompt: pitahaya-draak fase 2 (teju), startprompt v1 (16 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn en besluiten: `docs/concept/IDEEEN.md` (Pseudo-legendary draak: pitahaya).
Bijlagen (Jordi zelf toevoegen): (1) de fase 1-sprite `../../pitahaya_draak/af/pitahaya_draak_8x.png`, (2) een foto van een teju met open bek (Argentijnse teju, *Salvator merianae*), (3) een foto van een doorgesneden roze pitahaya (wit vruchtvlees met zwarte pitjes).

## Jordi (letterlijk, 16 nov)
- "dan is fase 2 een teju en fase 3 mag op 2 poten staan, maar voorover leunend, komodo draak"
- "Het gezicht zit in de vrucht bij fase 1, maar daarna komen er meer kenmerken bij"
- "het vruchtvlees wil ik wel erin hebben, ik twijfelde tussen buikpatroon of de binnenkant van de mond" → mond: "ja dan moet de bek groot open"
- "Ik wil duidelijk de dragonfruit blijven laten tonen"
- "Ik wil laag op vier poten, net wat gemener, duidelijke middenfase, beetje grootte als gabite, maar gabite staat op 2"

## Keuzes Claude (schrappen mag)
- Roze schil met groene schubpunten op kop en rug, poten en staart groene cactusrank (zoals fase 1: roze kop, groen lijf).
- Grootte in woorden in plaats van "Gabite" (een genoemde Pokémon kopieert Gemini).

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The second stage of a three-stage dragon line (pseudo-legendary). The attached sprite is STAGE 1: a pink dragon fruit (pitahaya) head on a small green cactus-stem body. Use it only for the colors and materials; do not copy its body shape or face.
- Stage 2 is a tegu lizard (Argentine tegu, see the attached photo): low on four legs, heavy head with thick jaws, long thick tail.
- It must still clearly read as a pink dragon fruit: hot pink skin with green-tipped scale flaps on the head and back. Legs and tail are the green pitahaya cactus stem (three-ribbed, wavy edges), like the stage 1 body.
- The mouth is wide open, hissing. The inside of the mouth is the white dragon fruit flesh with small black seeds, so the open mouth looks like a cut dragon fruit (pink rim around white seeded flesh, see the attached photo).

DESIGN
- A clear middle stage: bigger and meaner than stage 1, not yet a final dragon.
- Slightly mean, threatening expression.
- Colors: hot pink, green scale tips, green stem, white flesh with black seeds in the mouth. Keep it simple.

POSE
- Three-quarter view facing left, low on all four legs, mouth wide open.
- Compact Gen 3 composition: body and tail fit in a square, legs close to the body.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature filling about three quarters of the canvas, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO floor, shadow, base platform, leaves, glow or effects. One single creature, no extra views.

AVOID
- Not standing on two legs. Not a snake. No wings.
- Not a realistic lizard with a fruit stuck on it: the dragon fruit is its skin.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

---

# Prompt v2 (16 nov): zelfde gesprek, reactie op r1 (`r1.png`)

## Jordi (letterlijk)
- "design is tof, misschien net iets te weinig de vrucht zelf?" · vraag: "is de grootte goed voor een sprite?"

## Claude
- Vrucht: alleen de kop is vrucht; het lijf is een groene hagedis met roze stippen. Voorstel: rug roze schil met groene schubpunten (zoals de kop), stippen weg, poten en staart groen.
- Grootte: te breed (±2:1); in 64×64 wordt hij een smalle streep met een klein kopje. Voorstel: meer naar de kijker gedraaid, staart opgekruld naast/achter het lijf, past in een vierkant.
- Max. 2 wijzigingen per bijlageronde (GEMINI.md); bek, kop en kleuren expliciet behouden.

```
The design is good: keep the head, the wide open mouth with the white seeded flesh, the expression and the colors exactly as they are. Change only two things:

1. More dragon fruit on the body: the back (from the neck to the base of the tail) becomes the same hot pink dragon fruit skin as the head, with a row of green-tipped scale flaps along the spine, like on a real pitahaya. Remove the small pink dots. Legs, belly and tail stay green cactus stem.
2. Compact Gen 3 sprite composition: it must fit in a 64x64 square. Turn the body more towards the viewer (three-quarter view facing left, seen more from the front), shorten the body, and curl the tail up and around beside the body instead of stretching it out behind. Same pose otherwise: low on four legs, mouth wide open.
```
