# Vuurwerkslang, fase 3 van de vuurwerklijn (SPEC)
Fire/Fairy. Lijn (2 fases, Jordi 19 nov): vuuraxolotl (`../vuurwerk_fase1/af/`) → vuurwerkslang (deze; map heet nog `fase3`). Naam open. Hele ontwerpgeschiedenis en citaten: `docs/concept/IDEEEN.md` (Vuurwerk) en `docs/concept/sprites/vuurwerk/` (prompts v1–v14, rondes r1–r11).

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

## Rondes (Jordi letterlijk, 16 nov)
- r4: "de ogen zijn nog niet zo goed zichtbaar, binnenkant misschien een andere kleur geven die losse vlam rechtsbovenin is een lijn geworden. Als je ruimte hebt mag de kop ook best groter. Ik vind hem verder nog niet slecht hoor." · "desnoods doe je de oogkleur niet wit zodat je meer contrast hebt"
- r5: "de kop 115% prima, maar het belangrijkste is dat het oog groter wordt. ik zie geen pupil nu"
- r6 (Seviper-oog): "nee vreselijk, het oog was bijna goed en nu compleet verknald"
- r7: "het leest nog niet goed het oog he, verder is een bovenste stuk vlam nu een vierkant" · "ja het linkeroog is sowieso een blur, het moet zodanig worden dat er echt een oog uit te halen valt, dat is bij r5 115% nog het beste alleen die heeft dus geen pupil"
- r8: "ik heb echt geen idee wat je met het linkeroog aan het doen bent, rechteroog lijken a en b allebei prima"
- r9: "nee het gebied links moet gewoon wat gefixed worden, er moet niet een extra oog bij"
- r11: "blijkbaar snap je niet wat ik met linkeroog bedoel, ik heb hem omcirkeld" (`referenties/jordi_linkeroog_omcirkeld.png`: het gebied uiterst links aan de koprand, de bruine dubbele lijn met de tan strook, ±x3–6, y18–24).
- r14: "allemaal slecht, ik heb hier puntjes op 3 potentiele pixels gezet die mogen veranderen, de rest blijft hetzelfde" (`referenties/jordi_linkeroog_puntjes.png`; gemeten: (4,22), (4,23), (5,24) op r12 p2). r15 = 8 combinaties van alleen die 3 pixels (`sprite/r15/`).
- r12: "deze vlam hier is aan de onderkant een rechte lijn, daar mag iets meer contrast in, misschien 1 of 2 pixels anders" (`referenties/jordi_vlam_rechtsboven.png`); varianten A–D in `sprite/r16/`.
- Vlam rechtsboven: Jordi kiest "B" → `sprite/r16/sprite_B.png` = eindsprite-kandidaat (r12 p2 + (43,6) leeg, (41,6) donkerrood).
- Na "af": "linksbovenin is een afgekapt stuk vuurwerk, maar dat gaat er raar uitzien in een gevecht denk je niet?" → varianten in `sprite/r18/`.
- r18: "beter, ik vind het vuurwerk onderin er mooi uit zien, maar het lijkt nog niet echt een verband te hebben met de rest van de sprite he" → varianten A–C in `sprite/r19/`.
- r19/r20: "nee het gaat me niet direct om de positie, maar we moeten nadenken wat het verband is" · "pokemon hebben over het algemeen geen special effects, dus daarom twijfel ik" → `sprite/r20/sprite_1_zonder_barst.png` (losse barst weg).
- Jordi: "ja hij is beter zonder, zorgt ook voor minder ruis waardoor de sprite beter leest" → r20 zonder barst = af.
