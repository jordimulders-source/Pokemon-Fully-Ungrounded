# Blobfish fase 1, sprite r1 (maker)

Methode: Krassault (model overnemen, niets tekenen). Een eerste poging met oppervlak-middeling (`basis.py`) is weggegooid op aanwijzing van Jordi ("ga niks zelf tekenen, volg de krassault en andere goede sessies").

## Stappen
1. `natief.py` (kopie van `sneeuwbolslak_fase2/sprite/natief.py`, pitchbereik 3,6–4,6): het Gemini-model heeft een raster van **4,0 px** → natief 255×163, vis **203×118**.
2. `half4.py` (afgeleid van `octillery_evo/sprite3/half2.py`): **exacte 4×4-reductie met regels**. Elke spritepixel komt uit zijn eigen 4×4 modelpixels: achtergrond bij ≥ 8/16 wit (wit dat met de beeldrand verbonden is; wit binnen de vis is glans), oogwit/glans bij ≥ 3 witte px, lijn bij ≥ 4 donkere px (zwart of lijnrood volgens het model), anders de gemiddelde vulkleur → dichtstbijzijnde van 9 vultonen (k-means op de modelpixels, op echte modelkleuren gezet). Alle 16 fases (oy, ox) gemaakt; gekozen **oy=3, ox=2**: daar blijven het oog (donker boven, wit onder, zoals het model) en de mondlijn met het opgekrulde eind het best. Uitvoer: `kaal.png` (kale reductie) + `kaal_info.npz` (tellingen per blok).
3. `maak_r1.py`: alleen technische opschoning op `kaal.png` → `blobfish_r1.png`; elke wijziging staat in `afwijkingen.txt`.

Hulpmiddelen: `blok.py` (modelmeting per spritepixel uit het 4×4-blok), `raster.py` (natief model met spriteraster erover naast de sprite), `toon.py`, `vel.py`.

## Maat
Gen 3-basisvissen (frame 1): Barboach 638 px (32×42), Feebas 767, Remoraid 606, Chinchou 761 (56×33), Carvanha 1089, Magikarp 1038, Goldeen 1184, Wailmer 1252 (50×35, ligt ook plat), Corphish 1047; eindvormen Whiscash 1286, Sharpedo 1294, Relicanth 1427.
Gekozen: de 4×-reductie zelf, **50×29, 848 px** (tussen Feebas en Magikarp; past bij fase 1 van 2, vult de breedte niet helemaal). 3× zou 68 px breed zijn (te breed, ±1500 px = eindvormmaat). Onderste rij **y = 54** (Barboach 52, Whiscash 54, Magikarp 57), x 7–56.

## Kleuren
10 + transparant: zwart (48,12,14), lijnrood/selout (90,34,36), lijf 3 tinten (153,42,49) (166,46,50) (181,47,47), schaduw-mauve (169,68,74), lip/vin 3 tinten (202,75,73) (185,112,112) (222,144,150), oog/glanswit (219,203,203). Allemaal kleuren uit het model. Palet-index 3 en 5 staan nog in het palet maar worden niet gebruikt.

## Afwijkingen van de kale reductie (217 van 848 px)
| Stap | Reden | gezicht (ogen+lippen) | kop/lijf | rugvin | borstvin | staart | totaal |
|---|---|---|---|---|---|---|---|
| A | palet: tint (144,42,47) en (153,42,49) zijn in het model bijna gelijk (helderheid 73/76) → samengevoegd; zichtbaar verschil ≈ 0 | 47 | 34 | 0 | 2 | 4 | 87 |
| B | buitenlijn 1 px: zwart aan de schaduwkant (onder/rechts), selout lijnrood aan de lichtkant, geen glans/lichte kleur op de rand, geen zwart/selout om en om (rand nu 53% zwart; Gen 3-rode soorten 25–49%, model onder/rechts dik zwart) | 22 | 30 | 6 | 3 | 29 | 90 |
| C | ruis: losse vulpixels (cluster van 1) in de lijf-/schaduwtinten nemen de meest voorkomende buurtint aan; lichte tinten (vinstralen, lipglans), lijnen en wit bevroren | 7 | 14 | 1 | 0 | 17 | 39 |
| D | verre oog (10,41): pupil viel weg in de reductie; modelblok heeft 3 donkere px, mediaan (92,42,44) → lijnrood | 1 | 0 | 0 | 0 | 0 | 1 |

Zones (spritecoördinaten x0,y0–x1,y1): gezicht 6,36–30,55; kop/lijf 6,30–40,55 (buiten het gezicht); rugvin 28,26–40,36; borstvin 28,36–42,56; staart 40,24–58,40.
Zonder stap A (alleen indexwissel naar een bijna gelijke kleur) zijn het **130 px**, waarvan 90 buitenlijn.

## Gezicht (12× naast het model, vel.png)
- Lippen: bovenlip licht met glans linksboven (x 8–15, y 45–48), zwarte mondlijn y 48–49 van x 10 tot 19, opgekruld eind en ronde lipeind-lijn op x 20–21 (y 48–50), onderlip y 50, zwarte onderliplijn y 51, kin y 52, buitenlijn y 53. Alles uit de reductie, niets gezet.
- Ogen: nabij (19–20, 45–46) = 2 donker boven, wit rechtsonder (model: donker boven met glanspuntje, wit sikkeltje onder); ver (9–10, 41–42) = wit met donkere pupil rechtsboven (pupil = reparatie D). Op modelschaal (≈ 2 px); geen oog uit een andere sprite geleend.
- Neus: geen hangende neus; de bovenkop loopt rond over in de bovenlip, zoals het model.

## Zelf geziene zwakke punten
- **Contrast laag**: de lijftinten liggen dicht bij elkaar (helderheid 76/82/87), zoals in het model. Een Gen 3-licht/contrastronde (stappen ±30–40) mag volgens GEMINI.md pas met Jordi's akkoord; niet gedaan.
- **Lippen op 1× vrij donker/druk**: drie zwarte lijnen op 2 px afstand (mondlijn, onderliplijn, buitenlijn); alle drie zijn zwart in het model (gemeten: mediaan (48–74, 0–16, 0–16)). Links onder smelten onderliplijn en buitenlijn samen tot een donkere hoek (x 8–12, y 49–52). Het opgekrulde, blije eind van de mond leest wel op 2×.
- **Ogen klein**: het nabije oog leest op 1× vooral als donker stipje met één witte pixel; het verre oog ligt tegen de omtrek. Groter maken = afwijken van het model; vraag voor Claude/Jordi.
- **Vinstralen** zijn op 4× deels weggemiddeld (borstvin en staart houden lichte/mauve strepen, rugvin weinig).
- Een paar vulclusters van 2 px (tinten 6/7/8) zijn blijven staan; glans van 1 px (index 10/11/12) bewust gelaten.
