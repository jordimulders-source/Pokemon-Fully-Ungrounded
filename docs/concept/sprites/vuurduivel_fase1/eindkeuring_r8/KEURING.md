# Eindkeuring r8 vuurduivel fase 1: schaduw, kleurtinten, belijning (`sprite_r8/vuurduivel_r8.png`)

Alleen de uitvoering gekeurd. Silhouet, ogen en de vorm van de staartpunt zijn bevroren. Het voorstel hieronder heeft alpha-diff 0 met r8 en verandert 11 pixels plus 2 paletkleuren.
Vel: `vel.png`: r8 8× | voorstel 8× | model; Houndour, Umbreon, Ponyta, Sableye, Spinda en Magcargo (Gen 3, `anim_front_gba.png`) op 8×; close-ups r8 tegenover het voorstel. Voorstel: `voorstel_r8_moet.png` (alle MOET-punten toegepast).

## Oordeel: **BIJNA** (na de MOET-lijst PASS)

Volume is in orde. De kop heeft een lichte bolling linksboven met glans (20–21,25–26), een sikkel in tint 2 rechts en onder, en de kin werpt een slagschaduw op de borst. De borst heeft glans (23–24,44). De broek bestaat uit twee dijen; de rechter heeft een lichte band op de bolling. Het haar loopt van oranje (licht, linksboven) naar rood (schaduw, rechtsonder). Tot de MOET-lijst horen kleine belijningsfouten en twee tintstappen.

### Gemeten tinten (helderheid L)
| Groep | Tinten | Stappen | Gen 3 ter vergelijking |
|---|---|---|---|
| Lijf (zwart) | lijn 16 · 2 = 39 · 3 = 63 · 4 = 94 · glans 133 | 24 / 31 / 39 | Houndour 35/51/76/128, Umbreon 43/59/84/136: goed |
| Broek (bruin) | b = 57 · B = 77 · c = 110 | **20** / 33 | Spinda 71/103, Sentret 74/110/142, Teddiursa 65/97/132 (±32–36): **b–B is te klein** |
| Vuur | R = 46 · r = 77 · m = 126 · O = 145 · Y = 208 | 31 / **49 / 19** / 63 | Ponyta 71/134/168/201: vier vuurtinten zijn Gen 3, maar **m staat bijna dubbel met O** |
| Roze | p = 129 (tong + hoornlicht) | — | goed, staat los van het vuur |

## MOET (alleen uitvoering; pixel (x,y) → tint)
1. **Middentint vuur**: paletkleur 12 m (226,88,62) → **(206,66,50)**, L 106. Stappen r→m→O worden 29/39 in plaats van 49/19 (nu bijna een dubbele tint met O).
2. **Donkerbruin broek**: paletkleur 9 b (76,51,36) → **(62,41,29)**, L 45. b→B wordt 32 (nu 20; b en B lezen nu bijna als één vlak).
3. **Rechterrand haar, schaduwkant open**: (38,25), (38,26) r → **R (108,19,20)**. Nu staat de basiskleur op de buitenrand en wisselt de rand R-R-r-r-R-R.
4. **Linkerrand haar om en om**: (18,20) r → **R**. Nu R-r-R; daarna loopt de rand netjes van R (onder) naar r (boven).
5. **Onderste rechter vlamtong, oranje op de schaduwrand direct boven R**: (38,21) O → **m**, (38,22) O → **r**, (37,22) Y → **O**. De rand loopt dan van oranje (punt) via m en r naar R, zoals Ponyta (oranje alleen op de punten, rood aan de schaduw-/onderkant).
6. **Linkerhand, zwarte klont (2×2 lijn)**: (16,47) L → **3 (66,62,62)**. (17,47) blijft L als vingerlijn.
7. **Linkerhoef, open randen + klont**: (22,58) B → **L** (open bovenrand; zoals (34,58) bij de rechterhoef); (21,59) c → **b** (lichte kleur op de buitenrand → gekleurde selout aan de lichtkant, zoals (34,59–61) rechts); (21,60) L → **b** (2×2 lijnklont in de teen).
8. **Losse donkere pixel links op de kop**: (18,27) 2 → **3** (een 2 tussen de lijn en het lichte vlak 4 leest als vlekje; de stap was 2 tinten).

## KAN
- Bovenrand van het haar en de staartpunt: O/Y op de buitenrand aan de lichtkant (bijv. (24,17), (25,16), (45,38) Y) mag, want Ponyta doet dat op zijn punten. Langs de rechterflank (38,18–20), (39,18–19) kan één tong meer naar r als je het vuur strakker wilt.
- Broek lichtkant: de linkerrand (19,51), (19,52), (18,53) is nu zwart; met b als gekleurde selout wordt die zachter (Gen 3-regel), maar bij zo'n donkere broek is het verschil klein.
- Punt van het linkeroor (12–13,29–30) is een 2×2 lijnblok; (13,30) → 3 laat de oorkleur tot in de punt doorlopen. Bij een scherpe punt is een dicht blok ook gebruikelijk (Sableye).
- Hoornpunten: links R (15,22), rechts L (26,21); gelijktrekken (beide R) maakt ze consistent.

## Ter info voor Jordi (geen keuringspunt)
- Geen.
