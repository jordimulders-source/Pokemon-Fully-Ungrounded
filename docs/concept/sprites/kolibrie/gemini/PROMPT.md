# Gemini-prompt: Soulibri opknappen (opknapronde, 19 nov)

Regels: `docs/lessen/GEMINI.md`. Stand: `../../OPKNAPRONDE_GEMINI.md`. Huidige sprite: `../af/kolibrie.png`. SPEC: `../SPEC.md`.

## Jordi (19 nov, letterlijk)
- "het model blijft, in tegenstelling tot curiqui ben ik volledig tevreden met het design van soulibri en picapau."
- **Soulibri:** "mag nog wat meer een typische kolibrie pose, maar behoud de kleuren en design"
- "Doe ook alvast een prompt voor Soulibri, gaan we vanavond mee verder"

Welke "typische kolibrie pose" is niet ingevuld: Gemini kiest (lessen: gedrag als posebron werkt; Gemini ontwerpt). Wil Jordi een bepaalde pose (zwevend, drinkend bij een bloem, zittend), dan één regel in POSE aanpassen.

## Bijlagen
1. `bijlage1_huidige_sprite_8x.png`: huidige sprite (design en kleuren; de pose mag NIET overgenomen worden, anders kopieert Gemini hem).
2. `bijlage2_anatomie_kolibrie.png`: Jordi's anatomiefoto (`../referenties/jordi_anatomie_mango.png`), alleen voor de kolibrie-anatomie. Voorstel Claude; weglaten kan.

Nieuw gesprek per poging; bijsturen hooguit 1–2 keer.

## Prompt v1

```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), drawn fresh as a Game Freak artist would.

ATTACHMENTS
- Attachment 1 is the current sprite of this Pokémon. KEEP its design and its colors exactly. Only the POSE must change: do NOT trace or copy its pose, its side view or its silhouette.
- Attachment 2 is a photo of a real hummingbird, ONLY for hummingbird anatomy (how the wings, body, tail and beak connect). Do not copy its colors.

THE CREATURE (keep this design)
- A Ghost/Flying hummingbird Pokémon from the Andes, a gentle soul guide (a positive link with death and the afterlife, mystical, not scary).
- Head: velvet-black, like Ho-Oh or Fearow in head style, with a small eye. A crest of three long feathers swept up and back (a Guaraní feather crown).
- Long, thin, straight hummingbird beak.
- Body: iridescent velvet violet with a blue-green (teal) sheen on the shoulders.
- Wings: pale lavender, becoming gradually more translucent from the middle to the outer edge (like Venomoth's wings). Exactly two wings.
- Tail: long streamers trailing behind with Articuno-like dynamics, ending in pale little soul-flame racket tips.

POSE (the only thing that changes)
- A more typical hummingbird pose, as a real hummingbird would hold itself.
- Front sprite composition: compact enough to fit a square, head on the left.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites, large calm shading areas, no noise.
- Plain white background. No flower, branch, ground, rock, shadow or base.
- No sparkles, glow, motion lines, text or effects. One single creature, no extra views.

AVOID
- Do not change the colors or add new features. Not Ho-Oh, Fearow, Xatu or Ninjask with things added.
- No plush toy, chibi, Neopets or mascot look; no big eyes.
```

## Ronde 1 (Jordi, 19 nov, letterlijk): `r1_bijna.png` (prompt v1)
"wacht ik ben gelijk verder gegaan en deze is al bijna helemaal prima, alleen de snavel is nu te kort"

## Bijsturing r1 → r2 (zelfde gesprek)

```
Almost perfect. Keep everything exactly as it is: pose, head, crest, eye, body, colors, wings and tail. Change only one thing: the beak is too short. Make the beak a long, thin, straight hummingbird beak, clearly longer than the head, as long as in attachment 1, pointing in the same direction as now.
```

## Ronde 2 (Jordi, 19 nov, letterlijk): `r2_te_veel.png` (na bijsturing snavel)
"haha dit is weer too much" (snavel horizontaal en veel te lang; kuif en kop ook veranderd)

## Snavel zelf verlengen in r1 (Claude, 19 nov)
`verleng_snavel.py`: r1 blijft pixelgelijk; de snavelpunt schuift langs de eigen trapperiode van de snavel (16,16 px = 1 modelpixel diagonaal) en het gat wordt gevuld met kopieën van één plak van dezelfde snavel. Niets getekend. Varianten +2/+4/+6 modelpixels: `r1_snavel_k2.png`, `k4`, `k6`; overzicht `snavel_varianten.png` (r1 | k2 | k4 | k6). Jordi kiest.

## Keuze (Jordi, 19 nov, letterlijk)
"+2 is perfect. Dan is de sprite al zo goed als af toch? Gemini heeft het een keer in de goede artstijl gedaan"
→ bevroren als `../referenties/gemini_gekozen_r1_snavel_k2.png`.
Claude gemeten: Gemini-raster = precies 16 px per spritepixel (1:1 naar 64×64). r1 zelf was 64 px breed (snavelpunt x=0 tot racketpunt x=63); met +2 snavel is hij 66 px breed, 49 hoog: 2 px te breed voor 64×64. Kleuren: ±190 net verschillende tinten (JPEG-ruis + vleugelverloop) → naar ≤16.

## Jordi (19 nov, letterlijk), over de 2 px te breed
"we laten gemini de pose net iets anders maken"

## Prompt v2 (nieuw gesprek; bijlage: alleen `bijlage3_gekozen_r1_snavel_k2.png`)
Les: Gemini haalt geen exacte maat (sneeuwbolslak); daarom de beperking in verhoudingen beschrijven, niet alleen in pixels. Bijlage + "keep" = Gemini kopieert bijna letterlijk; dat is hier gewenst, behalve de kleine posewijziging.

```
This is a finished official Gen 3 front sprite of my Pokémon. I love it: keep its design, colors, art style, head, crest, eye, beak length, body, wings and tail exactly as they are.

Only one problem: it is slightly too wide. From the beak tip to the tip of the tail it is 66 pixels, but a Gen 3 front sprite must fit inside 64x64 pixels.

Change the pose just slightly so the whole creature fits inside a 64x64 square with a little room to spare, for example by angling the body or tail a little more. Keep the beak exactly this long. Do not shrink the creature and do not redraw it in another style: same pixel size, same pixel art.

Plain white background, max 16 colors, no effects, one single creature.
```
