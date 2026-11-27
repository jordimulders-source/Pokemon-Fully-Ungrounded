# Regionale Hitmonchan (ijssculptuur) – SPEC

## Besluiten (Jordi, 27 nov; letterlijk)
- "Hitmonchan ice, soort ijssculptuur met handschoenen als kubussen."
- Tyrogue blijft hetzelfde. Tegenhanger: regionale Hitmonlee van gloeiend glas (`../hitmonlee_regional/`).
- Open: puur Ice of Ice/Fighting; pose (prompt r1 = Hitmonchans eigen bokshouding).

## Gemini-prompt r1 (Engels, nieuw gesprek, zonder bijlage)
```
Design a regional form of the Pokémon HITMONCHAN, as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, clean dark outline, white background.

What it is: Hitmonchan as a carved ice sculpture. The whole body is made of clear ice, like a sculpture cut from a single block. It must clearly read as ICE, not plastic or glass:
- translucent pale blue and white ice, slightly darker blue in the thick parts and shadows;
- small sharp white highlights and a thin bright rim of light along the edges;
- some flat carved facets and chisel planes on the body, like an ice sculpture.
The boxing gloves ARE two big ice cubes: hard square blocks with straight edges and flat sides where the gloves would be, clearly cube-shaped, part of the body (not held, not separate objects).
Type: Ice.

Anatomy: keep Hitmonchan's body plan exactly (its head, its tunic, its legs and its arms), only the gloves become cubes. Two arms, two legs, one cube on each arm.

Pose: Hitmonchan's own boxing stance, facing 3/4 to the left, both cubes raised like boxing gloves. Compact composition that fits a square sprite; limbs close to the body.

No snowflakes, no frost particles, no mist, no glow, no effects, no pedestal, no ground, no shadow.
AVOID: a human in an ice costume, a statue on a pedestal, a snowman, a plush/Neopets look.
```

## r1 (beeld niet opgeslagen: kwam alleen inline)
- Glad lichtblauw Hitmonchan met twee glazige ijsklontjes als handschoenen.
- Jordi: "ok hij mag nog iets meer ijssculptuur lijken, nu is het een pallette swap met ijsklonten" / "gemini heeft ze ook letterlijk erop geplakt".

## Gemini-prompt r2 (nieuw gesprek, zonder bijlage)
Keuze Claude (ter controle): de kubussen zijn de onbewerkte stukken van het ijsblok waaruit hij is gehakt, zodat ze bij het lijf horen in plaats van erop geplakt.
```
Design a regional form of the Pokémon HITMONCHAN, as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, clean dark outline, white background.

What it is: an ice sculpture of Hitmonchan that came to life, carved with a chisel out of one big block of ice. It must NOT look like a smooth blue palette swap of Hitmonchan. It must look carved:
- the whole body is made of flat angular facets and chisel cuts with sharp edges, like a hand-carved ice sculpture at an ice festival; no smooth rounded skin anywhere;
- the head crest, the face, the tunic and the legs are roughly cut into planes, with visible chisel marks;
- clear ice: deep blue in the thick parts, pale cyan and white on the facets facing the light, frosted white on the rough cut surfaces, a few small white highlights on the sharp edges.
The fists were never carved: they are still the raw, uncut corners of the original ice block, so the forearms grow directly out of two rough cubic blocks of ice. Same ice, same facets, same color as the rest of the body, fused into the arms, not separate ice cubes stuck on.
Type: Ice.

Anatomy: keep Hitmonchan's body plan (head with its crest, tunic, legs, arms). Two arms, two legs, one block on each arm.

Pose: Hitmonchan's own boxing stance, facing 3/4 to the left, both blocks raised like boxing gloves. Compact composition that fits a square sprite; limbs close to the body.

No snowflakes, no frost particles, no mist, no glow, no effects, no pedestal, no ground, no shadow.
AVOID: smooth glossy body, plain recolor of Hitmonchan, ice cubes glued onto the hands, a human in an ice costume, a snowman, a plush/Neopets look.
```

## r2 (`gemini/r2.png`)
- Jordi: "iets beter maar de ijsklonten zijn opgeplakt, misschien een uppercut pose doen".
- Claude: blokken te groot en met een donkere scheidingslijn tussen onderarm en blok; facetten lopen niet door.

## Gemini-prompt r3 (nieuw gesprek, zonder bijlage)
```
Design a regional form of the Pokémon HITMONCHAN, as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, clean dark outline, white background.

What it is: an ice sculpture of Hitmonchan that came to life, carved with a chisel out of one big block of ice. It looks carved, not like a smooth blue recolor:
- the whole body is made of flat angular facets and chisel cuts with sharp edges, like a hand-carved ice sculpture; no smooth rounded skin;
- the head crest, the face, the tunic and the legs are cut into planes;
- clear ice: deep blue in the thick parts, pale cyan and white on the facets facing the light, frosted white on the rough cut surfaces, a few small white highlights on the sharp edges.

The fists are cube-shaped, and they are ONE piece with the arms:
- each forearm gradually widens and turns into the cube, like the sculptor carved the arm but left the fist as a rough square chunk of the original block;
- the facets and chisel cuts of the forearm run straight on into the cube; there is NO dark line, seam, cuff or gap between the arm and the cube;
- the cubes are the size of Hitmonchan's boxing gloves, not bigger, and the same ice and color as the arm.
Type: Ice.

Anatomy: keep Hitmonchan's body plan (head with its crest, tunic, legs, arms). Two arms, two legs, one cube-fist on each arm.

Pose: an UPPERCUT. The near arm drives straight upward, the cube-fist rising past the chin to above head height; the other arm stays bent close to the body, its cube-fist guarding in front of the chest. Knees bent, body twisting upward into the punch. Facing 3/4 to the left. Compact composition that fits a square sprite; limbs close to the body.

No snowflakes, no frost particles, no mist, no glow, no effects, no pedestal, no ground, no shadow.
AVOID: separate ice cubes glued or stuck onto the hands, oversized blocks, a dark outline between arm and cube, smooth glossy body, plain recolor of Hitmonchan, a snowman, a plush/Neopets look.
```

## r3 (prompt r3, uppercut)
- Jordi (27 nov): "kijk dat werkt perfect". Uitgehakt ijs met facetten, kubusvuisten vloeien over in de onderarmen, uppercut met de verre arm omhoog, andere vuist voor de borst.
- Beeld kwam alleen inline binnen; voor de sprite moet Jordi het bestand nog als bijlage sturen (komt dan in `gemini/r3.png`).
- `gemini/r3.png` opgeslagen (Jordi: "vertaalt die naar een sprite?"). Test (Claude): raster 10,24 px duidelijk (score 2× hoger dan 5,12; natief schoon), figuur 50×81 cellen → ±79 % naar 64 hoog. Kale reductie in `test/` wordt vlekkerig in de facetten en het gezicht.
- Jordi (27 nov): "ok de ogen zijn het belangrijkst, die mogen niet kleiner, ga maar los" → ogen op modelgrootte (natief raster, niet verkleind), rest naar 64.
- Maker r7 → `sprite/kandidaat.png` (40×64, 7 kleuren, gezichtszone 1-op-1 op modelgrootte, rest ±76 %); eindkeuring loopt.
