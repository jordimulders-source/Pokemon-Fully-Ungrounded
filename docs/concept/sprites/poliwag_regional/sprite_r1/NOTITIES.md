# Regionale Poliwag (Ice/Poison) – sprite r1 (maker)

Model: `../referenties/gemini_gekozen_v2.png` (bevroren, Jordi 25 nov). Uitvoer: `poliwag_regional_r1.png` (64×64, geïndexeerd, index 0 transparant), `vel.png`.

## Aanpak (overnemen, niet hertekenen)
1. **Natief raster gemeten** (`meet.py`): randsterkte per kolom/rij → periode **15,36 px** (= 1024/66,7), horizontaal en verticaal gelijk. Een adaptief raster (celgrenzen op pieken) liep scheef; een **vast raster met de fase met de hoogste materiaalzuiverheid** (fase 5,0 / 5,0, zuiverheid 0,86) viel goed op de modelpixels (`reduceer.py`).
2. **Kale reductie** (`reduceer.py` → `kaal.npy`, `kaal_8x.png`): elke modelpixel krijgt een materiaal (lucht / geel / rood / ijs / donker); per cel wint het meerderheidsmateriaal, de tint is de dichtstbijzijnde paletkleur van het gemiddelde van dat materiaal in de cel. Maat **50 × 41 px** (Poliwag gba: 49 × 26 breed/hoog), in het 64-vak op x 7–56, y 19–59.
3. **Opbouw** (`build.py`, alles herhaalbaar):
   - A: tinten per materiaal uit de **modelhelderheid**. Lijf (zwart met grijze spikkels): helderheid gladgestreken over σ 1,5 cel = de toegestane opschoning van de spikkels; grenzen volgen daardoor het lichtveld van het model (licht onder de kop en naast de schijf, donker naar rechts), gebogen. Geel σ 1,0; ijs (schijf, staart, kristallen) vrijwel per cel (σ 0,45), zodat de lichtrand en glanspixels van het model blijven.
   - B: omlijning (technisch): lijf/poten zwart; geel aan de lichte kant donkergeel (de selout die het model zelf heeft), aan de schaduwkant zwart; schijf tegen lucht zwart (model); staartvin boven/links ijs-donker (11), onder/rechts ijs-donkerst (15), zoals het blauwgrijze randje van het model.
   - C: reparaties per pixel naar het model (zie hieronder): spiraal, ogen, mond (rood), kristallen, staartkern, ruiscellen.
4. Meet- en controlegereedschap: `celinhoud.py` (samenstelling per cel: zwart/wit/ijs/geel/rood), `rasterbeeld.py` en `naast.py` (model met spriteraster), `controle.py` (kleuren, clusters < 3 px, lichte pixels op de buitenrand), `afwijking.py` (per zone t.o.v. de kale reductie), `vel.py`, `toon.py`.

## Kleuren: 15 + transparant
| idx | kleur | gebruik |
|---|---|---|
| 1 | 16,16,24 | omlijning, pupil, mondspleet |
| 2 / 3 / 4 | 40,40,52 · 58,58,74 · 88,88,108 | lijf schaduw / basis / licht (waarden zoals Umbreon/Houndour gba), poten 3/4 |
| 5 / 6 / 7 | 248,240,128 · 232,204,48 · 168,136,24 | geel licht / basis / donker + selout |
| 8 / 9 / 10 / 11 / 15 | 240,248,248 · 192,226,240 · 144,190,216 · 88,136,168 · 52,88,120 | ijs wit / licht / midden / donker / donkerst (selout) |
| 12 / 13 / 14 | 236,120,112 · 204,64,66 · 140,36,46 | rood licht (roze boog, glans) / rood / donkerrood |

## Afwijkingen per zone t.o.v. de kale reductie
"Andere index" = elke pixel met een andere paletindex (vooral tint/schaduw en omlijning); "ander materiaal" = pixel die een ander materiaal kreeg dan de modelcel (dat zijn de pixels die niet letterlijk uit de reductie komen).

| zone | px | andere index | ander materiaal |
|---|---|---|---|
| ver oog | 46 | 35 | 8 (waarvan 5 mond) |
| nabij oog | 64 | 29 | 6 |
| mond | 36 | 28 | 22 (kleur rood = Jordi) |
| kristal 1 / 2 / 3 | 35 / 17 / 18 | 22 / 9 / 13 | 6 / 4 / 8 |
| schijf + spiraal | 330 | 85 | 23 |
| staart | 258 | 120 | 10 |
| poten | 73 | 38 | 0 |
| rest (kop geel, lijf) | 224 | 65 | 0 |
| **totaal** | 1100 | 444 | 87 |

**Elke pixel die niet uit de reductie komt (materiaalwissel), met reden:**
- **Ver oog:** (6,9) ijs→zwart (cel I4Z2, pupil bovenkant gesloten); (3,10) lucht→zwart (cel W7 maar met de zwarte modelrand; anders raakt het ijs de lucht); (5,13) donker→wit (cel W4G2: onderste ring). Ogen verder per cel uit `celinhoud.py`: pupil zwart met grijze onderkant, witte glans, ijsring links/onder.
- **Nabij oog:** (14,10) ijs→zwart en (16,10) zwart→wit: **glans 1 px naar rechts** – in het model raakt de 2 px glans de linker oogrand (cel W6Z2); in de sprite moet daar de omlijning staan, dus glans = (15,10)+(16,10). (17,13) zwart→wit (cel Z4W4, witte ring onder); (19,13) ijs→zwart en (18,14) geel→zwart: de onderrand rechts gesloten (in het model loopt daar een dunne schuine lijn); (15,14) donker→geel (cel Z3Y3). Het ijsstipje (15,9) bovenin de pupil staat in het model en is gehouden.
- **Mond (Jordi: vorm goed, kleur rood):** vorm 1-op-1 uit de modelcellen: rand bovenaan rij 12, kussen rij 13–16 (cols 7–12), spleet (8–9,14) en stip (10,15) zwart zoals het model, onderrand rij 17 zwart. Kleur: licht bovenin 12, onder 13, rand 14 (het rood van spiraal/staartkern). (12,13) donker→geel (cel Y6G2).
- **Spiraal (repareren: scherp, 1 px):** pad uit de rode modelcellen, 1 px lijn met 1 px tussenruimte, tegen de klok in naar binnen, buiteneinde rechtsonder (12,31) zoals het model. Weggehaald waar het model dikker/aaneengesloten is: (8–10,21) (bovenbalk was 2 rijen dik), (7,24), (11,24), (7,28), (10,28), (5,29), (14,30), (13,31) (lijnen raakten elkaar of waren 2 px). Toegevoegd als hoekpixel van hetzelfde pad: (7,23), (11,23), (6,24), (12,24). Roze boog linksboven (7,20), (6,21), (5,22), (4,23) = de lichtroze modelpixels (de reductie las die als ijs/donker). Midden = modelvorm (8–10,25) + (10,26–27). (7,21) grijze ruiscel → ijs.
- **Schijf:** (2,29) ijs→zwart (omlijning tegen lucht); (9–12,34) donker→ijs-donkerst: de donkerblauwe onderrand van het model (celkleur 65,101,114) die de reductie als "donker" las.
- **Kristallen:** silhouet en rood uit de cellen; (20,2) weg; (24,1), (24,6), (28,7), (28,8), (30,14), (32,15), (32,16) = de blauwgrijze modelrand (in de cel minderheid naast lucht); (24,4), (24,5), (27,9), (31,18), (30,19) = de donkere modelrand (las als "donker") → selout 15. Rood: (21,3) licht, (22,4), (20,5), (21,6), (22,6) donker; (26,8–9); (30,16–18) – alle uit de cellen met R in `celinhoud.py`. (21,1) losse ijscel weg.
- **Staart:** rode kern per rij exact op de cellen met rood (`celinhoud.py`), schaduw per cel uit de modelkleur (licht 12 alleen waar het model ≥ 215 rood heeft, rij 20–25); (38,25), (35,27), (33,28) donker→rood (cellen met donkerrood "."+R). Rand rechts (49,18–20), (43,27), (41,28), (39,29), (31,29) = donkere modelrand → selout. Vier losse tintcellen in de vin gelijkgetrokken met de buur ((39,21), (37,22), (41,23), (35,24), (33,24), (39–40,27), (40,18)).
- **Lijf, kop, poten:** 0 materiaalwissels; alleen tint (lichtveld uit het model) en omlijning.

## Vergelijking (vel.png)
Naast Poliwag (gba), Ninjask (geel-zwart) en Dundragoon (maatstaf): lijfwaarden zoals Gen 3-zwarte soorten (Umbreon/Houndour), omlijning 1 px, zwart aan de schaduwkant, donkergele selout bovenop de kop, ijs-selout om vin en kristallen. Op 1× lees je kop, ogen, rode mond, spiraal en staart.

## Eigen zwakke punten (na eigen reparatie)
Al gerepareerd in deze ronde: lijf te grijs (te lichte basis + groot lichtgrijs vlak onder de kop → basis donkerder, licht 4 nog maar een paar px); staartkern te roze (licht rood alleen nog waar het model licht is); open rand bij kristal 1 ((21,2) wit aan de lucht); losse grijze ruiscellen in vin en schijf.

Nog open, ter beoordeling:
1. **Spiraal oogt hoekiger dan in het model** (rechte stukken van 3–4 px). Het pad komt uit de modelcellen; het model is alleen ronder door anti-aliasing. Ronder kan alleen door de 1/1-lijnafstand op enkele plekken los te laten.
2. **Mond leest groter/zwaarder dan het lichtblauwe modelkussen**, door rood met donkerrode rand naast geel. Vorm is gelijk; als het te zwaar is, kan de rand (14) lichter.
3. **Glans nabij oog 1 px rechts van het model** (zie boven), omdat de oogrand dicht moest.
4. **Kristal 1 is druk** (twee punten met verspreide rode spikkels): zo staat het in het model; niet vereenvoudigd.
5. **Rechterkant van het lijf (col 29, rij 18–25) is een rechte verticale rand**: staat zo in het model (achter de staart); niet rond gemaakt.
