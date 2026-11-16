# Vuurwerkslang, fase 3 van de vuurwerklijn (SPEC)
Fire/Fairy. Lijn: sterretje → wondertol → vuurpijl (deze). Naam open. Hele ontwerpgeschiedenis en citaten: `docs/concept/IDEEEN.md` (Vuurwerk) en `docs/concept/sprites/vuurwerk/` (prompts v1–v14, rondes r1–r11).

## Model (bevroren ontwerp)
`referenties/model_v14.png` (Gemini v14). Jordi, 16 nov: "dit vind ik de beste tot nu toe, het is nog steeds geen vuurwerkhoofd, maar wel dynamisch. Hoe de kleur geleidelijk verandert is ook vet".
Meting Claude: Gemini-raster ±10,24 px (100×100); dier ±69×72 natieve pixels → ±10% kleiner voor 64×64.

## Jordi letterlijk (sprite)
- "lukt het om hier een sprite van te maken?"
- "wat ik dan aanraad is dat we om het hoofd heen dan vuurwerk spikkels doen"
- "die glitterspikkels kan je wegdoen en dat worden dan vuurwerkspikkels"
- Eerder: "laten we niet meer vragen ook aan gemini om vuurwerk explosies te maken, want dat kan die niet"; vuurwerk zoals `referenties/vuurwerk_pixelart_jordi.png`: "dit is vuurwerk imo".

## Toegestane afwijkingen van het model (alleen deze, als bovenlaag)
1. De glitterspikkels in het lijf weg; daar komen vuurwerkspikkels voor in de plaats.
2. Vuurwerkspikkels om het hoofd heen.
Stijl van de spikkels: `referenties/vuurwerk_pixelart_jordi.png` (losse, onderbroken stralen van ongelijke lengte, felle pixels langs en aan het eind, onregelmatig, geen omlijning, klein of geen fel midden).

## Niet besloten (niet doen)
- Barsten op het lijf (niet gevraagd).
- Frame 2, rug, icoon, shiny, naam/data: later voor alle soorten samen.
