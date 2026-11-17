# Gemini-prompt: pitahaya-draak fase 3 (komododraak), startprompt v1 (17 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn en besluiten: `docs/concept/IDEEEN.md` (Pseudo-legendary draak: pitahaya).
Fase 1: `sprites/pitahaya_draak/af/` · Fase 2 (teju): `sprites/pitahaya_draak_fase2/af/` (model `model/model.png`, keuzes in `SPEC.md`).
Bijlagen (Jordi zelf): fase 1-sprite (`pitahaya_draak/af/pitahaya_draak_8x.png`), fase 2-sprite (`pitahaya_draak_fase2/af/pitahaya_draak_fase2_8x.png`) en een foto van een komodovaraan.

## Jordi (letterlijk)
- 16 nov: "dan is fase 2 een teju en fase 3 mag op 2 poten staan, maar voorover leunend, komodo draak"
- 16 nov: "Het gezicht zit in de vrucht bij fase 1, maar daarna komen er meer kenmerken bij"
- 16 nov (fase 2): "Ik wil duidelijk de dragonfruit blijven laten tonen"
- 17 nov: "fase 3 van de dragonfruit draak. Komodo draak" · "jawel, de teju is wel af"

## Keuzes Claude (schrappen mag, niet besproken)
- Materialen van fase 2 doorgezet: roze schil met groene schubpunten op kop en rug, poten en staart groene cactusrank.
- Open bek met wit vruchtvlees en zwarte pitjes, zoals fase 2.
- Eindvorm van een pseudo: groot en zwaar. Geen vleugels.
- Kijkt naar links, driekwart, dreigend.

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The final (third) stage of a pseudo-legendary dragon line based on the pink dragon fruit (pitahaya). The two attached sprites are stage 1 (a pitahaya head on a small cactus-stem body) and stage 2 (a tegu lizard low on four legs). Use them for the colors, materials and the mouth; do not copy their body shapes.
- Stage 3 is a Komodo dragon (see the attached photo): heavy monitor-lizard body, long thick neck, long heavy head, thick tail. It stands on its two hind legs but leans forward: body angled forward, not upright like a human, tail as counterweight.
- It must still clearly read as a pink dragon fruit, like stage 2: hot pink skin with green-tipped scale flaps on the head and back; legs and tail are the green pitahaya cactus stem (three-ribbed, wavy edges).
- The mouth is open, the inside is white dragon fruit flesh with small black seeds, like stage 2.

DESIGN
- A fully grown pseudo-legendary: big, heavy and powerful, clearly more than stage 2. Reads as a dragon first, not as a fruit with legs.
- Colors as stage 2: hot pink, green scale tips, green stem, white seeded flesh in the mouth. Keep the palette limited.
- Readable silhouette: forward-leaning two-legged monitor lizard with a long heavy tail.

POSE
- Three-quarter view facing left, threatening.
- Compact Gen 3 composition: the whole creature fits in a square, tail curved beside or behind the body instead of stretched out.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature filling most of the canvas (it is a final stage), max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO floor, shadow, base platform, leaves, fire, glow or effects. One single creature, no extra views.

AVOID
- No wings. Not a snake. Not standing straight up like a human or a kaiju.
- Not Garchomp, Salamence, Tyranitar or Krookodile. Not a dinosaur (no T-rex).
- Not a realistic lizard with a fruit stuck on it: the dragon fruit is its skin.
- No glossy 3D render, no plush or mascot style.
```

---

# Prompt v2 (17 nov): NIEUW gesprek, reactie op r1 (`r1.png`)

## Jordi (letterlijk)
- "en het lichaam dan wat groener misschien? gewoon iets meer leuke ideeën om te onderscheiden van fase 2"
- "beetje too much overdesigned, plus qua ontwerp vertaalt die niet lekker naar een sprite. Ik zou het nog vet vinden als we nog iets van een dragonfruit bloem erin verwerken en de staart een knots heeft als een dragonfruit"

## Claude
- Nieuw gesprek (GEMINI.md: bijsturen werkt slecht bij grote wijzigingen), r1 niet als bijlage.
- Waarom r1 slecht vertaalt: ±2:1 breed (ondanks "fits in a square"), tientallen kleine schubflappen en vlekjes die op 64 px ruis worden.
- Ideeën van Claude om fase 3 van de teju te onderscheiden (luchtwortels, bloem als kraag/kam, driekantige rugplaten, gespleten tong van meeldraden); Jordi: "laten we allemaal proberen".
- Extra bijlage: foto van een pitahayabloem (groot, wit, nachtbloeiend).

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The final (third) stage of a pseudo-legendary dragon line based on the pink dragon fruit (pitahaya). The two attached sprites are stage 1 and stage 2 (a tegu lizard). Use them for the colors and materials; do not copy their body shapes.
- Stage 3 is a Komodo dragon: heavy body, thick neck, long heavy head. It stands on its two hind legs but leans forward (body angled forward, not upright), the tail as counterweight.
- The body is mostly green cactus stem (greener than stage 2). Hot pink dragon fruit skin with green-tipped scale flaps only on the head. Open mouth with white seeded dragon fruit flesh inside, like stage 2.
- The tail ends in a club shaped like a whole dragon fruit (pink, with green-tipped scale flaps).
- A dragon fruit flower (the large white night-blooming pitahaya flower, see the attached photo) as a collar around the neck or a crest on the head.
- Back plates: instead of scale flaps along the back, a row of three-ribbed green cactus stem segments with wavy edges, standing up like plates.
- Aerial roots, like the climbing pitahaya cactus uses to cling to trees: as a beard under the jaw or as strands hanging from the forearms.
- A forked Komodo tongue made of the yellow stamens of the flower.

DESIGN: SIMPLE, MADE FOR A SPRITE
- Few big, clear shapes, like official Gen 3 sprites (Salamence, Tyranitar, Flygon level of detail). Only a handful of large scale flaps, not dozens of small ones. No small spots, dots or texture on the skin.
- Big, heavy and powerful, clearly a final stage, but not over-designed.
- Colors: mostly green, with hot pink and white as accents. Keep the palette limited.

POSE AND COMPOSITION
- Three-quarter view facing left, threatening.
- It must fit in a SQUARE: about as tall as it is wide. The tail is short and thick, curled up beside or behind the body with the dragon fruit club raised; it does not stretch out sideways.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature filling most of the canvas, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO floor, shadow, base platform, leaves, fire, glow or effects. One single creature, no extra views.

AVOID
- No wings. Not a snake. Not standing straight up like a human or a kaiju.
- Not Garchomp, Salamence, Tyranitar or Krookodile. Not a dinosaur (no T-rex). Not an Ankylosaurus.
- Not a realistic lizard with a fruit stuck on it: the dragon fruit is its skin.
- No glossy 3D render, no plush or mascot style.
```

---

# Prompt v3 (17 nov): zelfde gesprek, reactie op r2 (`r2.png`)

## Jordi (letterlijk)
- "bloemkraag, cactussen op de rug weg, tong vertaalt ook nog niet helemaal lekker, lichaam is nu wat saai"
- "pose, staart en hoofd zijn prima"
- "roze op de rug en cactusribben in het lijf" (keuze uit: roze schubflappen op de rug, cactusribben in het lijf, lichte buik, meer luchtwortels)

## Keuzes Claude (schrappen mag)
- Tong: simpeler (kort, dik, twee punten, één kleur); Jordi heeft de tongvraag niet beantwoord.
- Vier wijzigingen in één ronde (meer dan de gebruikelijke 2); vaste delen expliciet genoemd.

```
Good. Keep the pose, the head, the tail with the dragon fruit club and the colors exactly as they are. Change only these things:

1. The flower becomes a collar: a ring of white pitahaya petals all around the neck, behind the head.
2. Remove the cactus plates on the back. Instead, a row of hot pink dragon fruit skin with green-tipped scale flaps along the spine, from the neck to the base of the tail, like on stage 2.
3. The green body is too plain: show the three-ribbed cactus stem in the body itself, as long ribs with wavy edges running along the body, legs and tail. Nothing sticks out.
4. The tongue: make it simple so it works in a small sprite: a short, thick forked tongue with two points, one yellow color.

Same Gen 3 sprite style, plain white background.
```

---

# Prompt v4 (17 nov): zelfde gesprek, reactie op r3 (`r3.png`)

## Jordi (letterlijk)
- "beter maar de bloem moet weg en de tong vraag ik me af hoe die naar sprite vertaalt"

## Claude
- Proef: r3 grof verkleind naar 64 px (`r3_proef64_8x.png`). De tong wordt een bleke streep van 1–2 px die met de tanden en het vruchtvlees in de bek samenvalt; nauwelijks leesbaar.
- Variant A (bloem weg, tong blijft) en B (bloem en tong weg); Jordi kiest.

A:
```
Better. Keep everything exactly as it is (pose, head, pink back, cactus ribs, tail with the dragon fruit club, colors). Change only one thing: remove the flower collar completely. The neck is green cactus stem like the rest of the body.
Same Gen 3 sprite style, plain white background.
```

B:
```
Better. Keep everything exactly as it is (pose, head, pink back, cactus ribs, tail with the dragon fruit club, colors). Change only two things:
1. Remove the flower collar completely. The neck is green cactus stem like the rest of the body.
2. Remove the tongue. The mouth stays wide open with the white seeded dragon fruit flesh inside.
Same Gen 3 sprite style, plain white background.
```
