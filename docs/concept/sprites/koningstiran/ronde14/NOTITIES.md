# Sapa Inca – ronde 14 (kleine reparatie op ronde 13)

Basis: `ronde13/sapa_inca.png`; **palet exact gelijk** (gecontroleerd). `sapa_inca.txt` = raster van ronde 13 met onderaan het blok "ronde 14", geschreven door `reparatie14.py`.
Bestanden:
- `sapa_inca.png/.txt`, `reparatie14.py` → `diff_per_punt.txt` (elke pixel RGB voor → na, plus de lijst losse pixels)
- `controle14.py` → `controle14_uitvoer.txt` (diff per zone, palet)
- `bouw.py` → `controle_uitvoer.txt` (open randen: alleen K, d en p naast transparant)
- `uitlijn.py` → `krabbel_punten.txt`, `uitlijning.npy`
- `vel.py` → `vel.png` (4× en 1× licht/donker naast ronde 13; alle zones op 12× naast ronde 13)
- `kijk.py`

Jordi: "minder mooi, het stuk met de rode lijn komt niet goed over, doordat het lichaam in die staf over gaat en de staf/staart daar maar 1 kleur is, evenals het uiteinde van de staf, die is nu gewoon weggeknipt". Daarna: "en de poten plus ertussenin is slordig", "evenals het linkeroog", "en boven de rechter vleugel zitten opeens een paar paarse pixels".

## Uitlijning krabbel (`uitlijn.py`)
`referenties/krabbel_jordi_staf_overgang.png` op ronde 13: **7,83 px per spritepixel, verschuiving x −1,5, y +11**. De rode lijn ligt op (17–18,47) → (18,48) → (18–19,49) → (19,50): precies waar het lijf in de staf overliep.

## Wat er veranderde
1. **Overgang staf/lijf** (6 px): een zwarte scheiding (K) loopt nu gebogen tussen staf en lijf: (19,47) → (19,48) → (17–18,49), daarna het lijf. De staf heeft daar 3 tinten plus vaan: licht y bovenaan (16,47), basis g (17,47), schaduw a (18,47) en de roestbruine vaan t eronder (17–18,48). Hij verdwijnt op dezelfde plek achter het lijf.
2. **Stafpunt** (19 px): spits en taps tot 1 px, zoals de puntige stafkop van ronde 9.
   - Vorm: zwarte top (15,16), dan 1 px lichtgoud y op rij 17–20 met omlijning d links en K rechts eromheen, op rij 20 een eerste donkergoud a, op rij 21 3 px (y, g, a), daarna de bestaande ruit.
   - De punt steekt 2 px over de kroon heen. Waar de afgeknipte punt van ronde 13 lag, is de kroon teruggezet zoals in ronde 9 (de veer eronder mist zijn vlek, zoals afgesproken).
3. **Poten** (13 px): beide poten hebben dezelfde opbouw: dij (d links, g/y licht, a schaduw, K rechts), een donkere zoomrij, scheen (d | g/y | a/K) en voet. De verre (linker) poot is donkerder, zonder y op de dij.
   - Rechts zijn het losse randpixeltje (34,56) en het hoekje (29,57) weg.
   - De linkervoet heeft een gesloten zwarte onderrand (21–25,61).
   - Tussen de poten is de ruimte schoon; alleen de staartaanzet (28,54) t / (28,55) K staat er nog.
4. **Verre oog** (1 px): vlak donker lid (23–24,23), pupil K (23,24), gouden iris (24,24) en nu een kleine reflectie a onder de pupil (23,25), net als bij het nabije oog. Zonder glans, want het ligt in de schaduw.
5. **Paarse pixels boven de opgeheven vleugel** (4 px): de onderste lavendelpixels van de kroonrand rechts (46,20) en (45,21) zijn schaduwrood geworden, met zwart ernaast ((47,20), (46,21)). De lavendel rand eindigt nu bij de gouden randvlek en hangt niet meer als stippen boven de vleugel.
6. **Los rood** (1 px): (31,25) naast het nabije oog → m.

## Controles
| Zone | px |
|---|---|
| 1 overgang staf/lijf (x14–21, y46–50) | 6 |
| 2 stafpunt (x12–17, y15–22) | 19 |
| 3 poten + ruimte ertussen (x20–35, y53–62) | 13 |
| 4 verre oog (x22–25, y22–26) | 1 |
| 5 paarse pixels (x40–50, y18–34) | 4 |
| 6 los rood (31,25) | 1 |
| **buiten de zones** | **0** |
- Silhouet +1 (25,61) / −2 ((34,56), (29,57)); totaal 1624. Palet identiek; 0 open randen; 15 kleuren + transparant.
- **Losse pixels** (hele sprite, geen buur in dezelfde kleurgroep, zwart niet meegeteld): in ronde 13: (24,24) gouden iris van het verre oog (los, geen goudbuur), (29,24) glans, (31,25) rood, (28,54) staartaanzet, (29,56) bruin aan de rechterdij; **na de reparatie alleen nog de bewuste**: (29,24) glans van het nabije oog en (28,54) de staartaanzet.

## Zelf gekeken (12× en 1× naast ronde 13)
- De staf loopt nu als aparte, ronde vorm achter het lijf in plaats van erin over te lopen, en de punt is weer spits. De poten zijn gelijk opgebouwd en de ruimte ertussen is schoon. Boven de vleugel staan geen losse paarse pixels meer.

## Eerlijk: wat nog niet klopt
- **Stafpunt:** de 1 px brede punt over de kroon (rij 17–20) leest op 12× als naald; op 1× is hij een dun streepje dat tegen het oranje van de kroon maar half opvalt.
- **Overgang staf/lijf:** het zichtbare stuk staf onder de hand is klein (5 px kleur). Op 1× zie je een gouden puntje met donker eromheen, niet echt een ronde staart.
- **Verre oog:** het blijft 2×2 px; op 1× een goudpuntje met donker lid. Groter kan niet binnen de kopmaat.
- **Poten:** de linkerscheen is 2 px kleur breed (het silhouet laat niet meer toe), dus "dezelfde opbouw" is links smaller dan rechts.

## Lessen
- Waar een staf achter een lijf verdwijnt, heb je een eigen donkere scheidingslijn nodig, ook als beide delen donker zijn; anders "loopt het lijf in de staf over" (Jordi).
- Een losse-pixelscan op kleurgroepen (niet op letters) vindt de slordigheden die een open-randcontrole mist.
