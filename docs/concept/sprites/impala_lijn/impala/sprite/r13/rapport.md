# Impala r13: poten (Jordi, 26 nov: "de poten zijn effen vlakken, controleer die opnieuw")
Basis r12 (= r11 + oog B3). Script `sprite/r13.py` (A) en `python3 r13.py B` (variant B). Vel: `r13/vel.png` (`r13/vel.py`).
Bevroren met assert (diff 0): alles buiten de vier pootvakken, silhouet (alpha), oogzone, strepen, witte borst/buik + grens; lijnen in A ongewijzigd behalve de hoefglans.

## Gemeten
- **Model:** per poot vlak. Binnenkant (model per derde van elke cel, zonder lijn): verre poten en nabije achterpoot 138–146, nabije voorpoot ~200; links/rechts verschil ≤ 5. Alleen de knie van de nabije voorpoot is iets donkerder (167–176, 2 rijen) en de hoeven hebben links een lichtere glans (80–120 tegen ~70). Er staat dus geen lichte voorkant / donkere achterkant per poot in het model; het volume komt uit het Gen 3-recept.
- **Gen 3 (_gba):** Stantler/Girafarig/Ponyta nabije poten 3–5 px vulling: lijn | lichte kolom | midden | (donker) | zwart; linkerlijn 74–110 helder. Verre poten (Stantler `1444444401`, Girafarig `12220`) zijn grotendeels één schaduwtint. Dunne poten met 1–2 px vulling (Skarmory `2b770`/`2970`, Dodrio `3880`/`0380`): lijn + één vultint, licht bij het gewricht; bij 1 px vulling past maar één tint. Hoeven (Stantler `260440`, Girafarig `2915530`): lichtere pixel links binnen de hoef.
- **Sprite:** de schenen van alle vier poten zijn 1 px breed (D | vulling | zwart): rijen 50–56 (verre voorpoot), 49–59 (nabije voorpoot), 50–55 (verre achterpoot), 51–58 (nabije achterpoot). Alleen bovenbenen, hakken en kogels zijn 2–5 px.

## Variant A (33 px)
Per rij en per poot: 1 px = middentint; 2 px = licht + midden; ≥ 3 px = licht + midden + donker. Tinten: nabije voorpoot H/L/N, nabije achterpoot L/N/M (basis van M naar N: model 145 ligt dichter bij N en hij staat vooraan), verre poten N/M/S. Vlakjes < 3 px (8-verbonden) terug naar de middentint. Hoefglans nabije voorpoot (31,61)(31,62) D → S.
Per poot: verre voorpoot 4, nabije voorpoot 2, verre achterpoot 3, nabije achterpoot 24. Kleuren: 12 + transparant.

## Variant B (47 px) = A + linkerlijn van de schenen van de twee nabije poten D → S
Gids: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts"; S (96) valt in de gemeten Gen 3-band voor de linkerlijn van nabije poten (74–110). Dat is een lijnwijziging, daarom een aparte variant.

## Oordeel: BIJNA, niet opgelost
Op de schenen is 1 px vulling, en daar past maar één tint. Licht, midden en donker naast elkaar kan alleen als de poot breder wordt (silhouet) of als de lijn verandert (variant B). Het verschil met r12 is op 1× klein. Daarom niet verder gaan zonder Jordi. **Ter info voor Jordi:**
1. A of B kiezen, of
2. de schenen 1 px breder maken (vorm uit het model: daar is een poot ±3 spritepixels breed tussen de lijnen). Dat verandert het silhouet en mag alleen met zijn akkoord.
