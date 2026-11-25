# Satelliet fase 1 – sprite r4 (maker; kleinere versie, ±950 px)

Jordi: "A, verklein maar naar ±950 px, maar alleen als alles er dan nog mooi uitziet". r3 blijft de terugvaloptie.

## Werkwijze
- `reduce.py 0.617 9 14`: dezelfde kale reductie als r1, maar dan rechtstreeks van `model/model_gekozen_natief.png` en niet van r3. Factor 0,617 uniform. Uitvoer: `kaal.npy` / `kaal.png`.
  - Kale reductie: 963 px, 46×41, x 9–54, y 14–54, onderkant op rij 54.
- `fix4.py`: alle reparaties op de kale reductie, elk met zone en reden. De volledige lijst per pixel staat in `afwijkingen.txt`. Het palet is gelijk aan r3 (10 kleuren, lijfstappen 30/42/45).
- Meetscripts:
  - `rond4.py`: cirkelfit en trappen van de bol.
  - `zwart.py`: 2×2 zwart, L-hoeken, K-D-K, open randen en losse vultintpixels.
  - `vel.py`: maakt `vel.png` en `sprite_8x_wit.png`.
  - `view.py` en `cel.py`: hulpjes.

## Resultaat
- **Dekking 985 px** (doel 900–1000), box 46×41, gecentreerd (x 9–54), zwevend met de onderkant op rij 54.
- 10 kleuren plus transparant, 16 paletplekken, index 0 transparant.

## Afwijkingen van de kale reductie (191 px)
| zone | px | wat |
|---|---|---|
| bolomlijning | 13 | selout aan de lichtkant overal D; (39,9) D→zwart |
| bolrand | 19 | reflectierand p→l; zwarte L-hoeken linksonder → vulling; losse w/l-pixels → W/m; rechtsboven (22,29) → D; onderrand (50,25) weg en (49,25) zwart (4 vlakke px werden 3, voor de rondheid); **(43,11) nieuw** |
| oog | 28 | buitenrand van de ring dicht: D aan de lichtkant, zwart onder/rechts. Ringvulling p. De donkere binnenring past op deze maat niet en is vulling geworden. Uitsteeksel van de pupil → iris. Pupilhoek (34,16) → iris, zodat de pupil 2-3-3-2 rond is. Zwarte hoekjes onder → P. |
| naad | 22 | 1 px in tint P; lip ernaast → w |
| voet linksboven | 5 | zwarte bovenkant → D, open rand → D, zwarte binnenpixel → P |
| voet rechtsboven | 9 | open bovenrand → D (onder andere twee lijftintpixels tegen transparant), linkerrand → D, 3 zwarte L-hoeken → vulling |
| voet rechtsonder | 5 | bovenkant/linksboven zwart → D, zwarte 2×2/L → P |
| antenne 1 | 22 | bovenrand D, onderrand zwart, lijnpixels binnenin → P; **5 nieuw** |
| antenne 2 | 18 | idem; **3 nieuw** (waarvan (21,38) bovenrand van de wortel); punt (16,54) → zwart |
| antenne 3 | 27 | idem; **9 nieuw**; wortel (36,38) → D |
| antenne 4 | 23 | idem; **5 nieuw**; wortel (47,36–37) → D |

**Pixels die niet uit de reductie komen: 23 nieuw, 1 weggehaald.**
- **Antenne 1 (5):** (19,33), (19,34), (20,30), (20,31), (21,29). Antenne 1 px verdikt aan de onderkant, langs de modelas.
- **Antenne 2 (3):** (21,47) en (22,45) onderaan, plus (21,38) aan de bovenrand van de wortel.
- **Antenne 3 (9):** (38,46)–(38,50) en (39,39)–(39,42), onderaan.
- **Antenne 4 (5):** (51,40), (51,41), (52,44), (53,46), (54,50), onderaan.
- **Bolrand (1):** (43,11). Met deze pixel wordt de trap linksonder het spiegelbeeld van die linksboven.
- **Weggehaald (1):** (50,25), aan de onderrand.

**Waarom de antennes verdikt zijn:** zonder de verdikking had ongeveer de helft van de antennekolommen maar 1 px kleur (D-1-zwart). Op deze maat blijft "geen 1 pixel lijnen" alleen overeind met 22 px reductieherstel.

## Metingen
- **Rondheid** (`rond4.py`): centrum (23,5; 35,6), r = 14,23.
  - Max afwijking per kwadrant: linksboven +0,33, linksonder +0,70, rechtsboven +0,38, rechtsonder +0,71 px (alle ≤ 0,8).
  - Trappen links, rijen per x: 1-1-1-1-1-2-2-**9**-2-2-1-1-1-1-1-1. Boven en onder zijn elkaars spiegelbeeld.
  - Trappen onderkant, kolommen per y: 1-1-1-1-1-1-2-2-3-3-3-2.
- **Zwart:** 159 px = 16,1 % (r3: 13,5 %; de kale reductie had 187).
  - 2×2 zwart alleen in de pupil.
  - L-hoeken alleen op knooppunten: (25,36) voet RB/antenne 2, (39,37) bol/antenne 3, (48,30) bol/voet RO, en in de pupil.
  - Geen K-D-K. Geen zwart aan de lichtkant: elk zwart pixel met lucht erboven zit aan een antennepunt of op de rechterflank.
  - Het hogere aandeel komt doordat de omlijning op deze maat verhoudingsgewijs meer ruimte inneemt. Zwart verder terugbrengen kan alleen door de onderranden van de antennes paars te maken, en dan zijn ze niet meer consequent met r3.
- **Open randen:** 0. **Losse vultintpixels:** 0.
- **Antennedikte** (kleurpixels per kolom): A1, A2, A3 en A4 hebben overal 2, op 3–4 px totaal. Alleen de punten zakken naar 1 px kleur (A1 kol 39–40, A3 kol 53, A4 wortel kol 36) of 0 (de eindkolom: A1 kol 41, A2 kol 54, A3 kol 54, A4 kol 53).

## Eerlijk oordeel (Jordi's voorwaarde "alleen als alles er dan nog mooi uitziet")
- **Bol en naad:** mooi rond, de naad leest goed als 1 px boog, het volume (hooglicht, sikkel) blijft. In orde.
- **Antennes:** lezen op 1× en 2× goed als 4 staafjes met een paarse bovenkant en een zwarte onderkant, geen 1-px-lijnen. Dat kon alleen met 22 px verdikking, en ze zijn daardoor relatief dikker dan in het model (verhouding antenne/bol groter dan in r3).
- **Oog:** leest op 1× en 2× als een oog: teal iris, ronde pupil, paarse ring, geen glans. Er is wel detail verloren. De donkere binnenring past niet meer, de iris is rondom maar 1 px, en het lichte teal is 3 px. In r3 is het oog duidelijk rijker. Dit is het grootste verlies.
- **Voetjes:** rechtsboven en rechtsonder blijven herkenbare knopjes. Het **voetje linksboven is bijna verdwenen**: het is nog maar een verdikking van 3 rijen aan de wortel van antenne 1 (in r3 een duidelijk knopje). Dat is een echt verschil met het model.
- **Zwart:** 16 % tegenover 13,5 % in r3. De sprite oogt op 1× daardoor iets "lijniger".

**Conclusie maker:** r4 is als kleine sprite netjes en heeft alle onderdelen. Maar "alles mooi" klopt niet helemaal: het oog verliest de binnenring en detail, en het voetje linksboven is nauwelijks nog een voetje. Op 1× in het gevecht valt dat weinig op; op 2× en 8× naast r3 wel (zie `vel.png`). Of dat binnen Jordi's voorwaarde valt, is zijn oordeel. Ik zou r4 alleen nemen als het formaat zwaarder weegt dan het oogdetail. Een tussenmaat (factor ±0,68, ±1150 px) zou voetje en oog waarschijnlijk redden; die heb ik niet gemaakt.

## Oplevering
`sprite.png`, `sprite.npy`, `sprite_8x_wit.png`, `vel.png` (r4 | r3 op 8×; r4 en r3 naast elkaar op 1× licht/donker/groen en op 2× licht/donker; oog r4 op 12× naast het model op dezelfde schaal), `afwijkingen.txt`, scripts. Geen git.
