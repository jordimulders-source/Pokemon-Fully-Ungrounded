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
- "beetje too much overdesigned, plus qua ontwerp vertaalt die niet lekker naar een sprite. Ik zou het nog vet vinden als we nog iets van een dragonfruit bloem erin verwerken en de staart een knots heeft als een dragonfruit"

## Claude
- Nieuw gesprek (GEMINI.md: bijsturen werkt slecht bij grote wijzigingen), r1 niet als bijlage.
- Waarom r1 slecht vertaalt: ±2:1 breed (ondanks "fits in a square"), tientallen kleine schubflappen en vlekjes die op 64 px ruis worden.
- Plek van de bloem: niet ingevuld, Gemini laten kiezen (Jordi zei alleen "erin verwerken").
- Extra bijlage: foto van een pitahayabloem (groot, wit, nachtbloeiend).

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The final (third) stage of a pseudo-legendary dragon line based on the pink dragon fruit (pitahaya). The two attached sprites are stage 1 and stage 2 (a tegu lizard). Use them for the colors and materials; do not copy their body shapes.
- Stage 3 is a Komodo dragon: heavy body, thick neck, long heavy head. It stands on its two hind legs but leans forward (body angled forward, not upright), the tail as counterweight.
- Hot pink dragon fruit skin with green-tipped scale flaps on the head and back; legs are green cactus stem. Open mouth with white seeded dragon fruit flesh inside, like stage 2.
- The tail ends in a club shaped like a whole dragon fruit (pink, with green-tipped scale flaps).
- Somewhere in the design, a dragon fruit flower (the large white night-blooming pitahaya flower, see the attached photo).

DESIGN: SIMPLE, MADE FOR A SPRITE
- Few big, clear shapes, like official Gen 3 sprites (Salamence, Tyranitar, Flygon level of detail). Only a handful of large scale flaps, not dozens of small ones. No small spots, dots or texture on the skin.
- Big, heavy and powerful, clearly a final stage, but not over-designed.
- Colors: hot pink, green, white. Keep the palette limited.

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
