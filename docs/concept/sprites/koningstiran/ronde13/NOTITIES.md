# Sapa Inca – ronde 13 (top 5 uit EINDKEURING.md)

Basis: `ronde12/sapa_inca.png` (ronde 10 + goudstaf). Het **palet is exact dat van ronde 10/12** (gecontroleerd); er is niets geschaald of verplaatst. `sapa_inca.txt` = het volledige raster van ronde 12 met onderaan het blok "ronde 13", geschreven door `reparatie13.py`.
Bestanden:
- `sapa_inca.png/.txt`, `reparatie13.py` → `diff_per_punt.txt` (elke pixel met RGB voor → na)
- `controle13.py` → `controle13_uitvoer.txt` (diff per zone, palet, 2×2-klonten)
- `bouw.py` → `controle_uitvoer.txt` (open randen: alleen K, d en p naast transparant)
- `vel.py` → `vel.png` (4× en 1× licht/donker naast ronde 12; kop, flank en staf op 10× naast ronde 12)
- `kijk.py`

## Wat er veranderde (palet-letters: K zwart, d (52,38,36), m (88,66,58), l (136,104,86), r (186,54,34), o (250,162,92), a (172,104,34), g (230,172,58), y (250,226,132), b (112,128,152), w (210,222,234), t (162,82,42))
1. **Ogen en snavel** (6 px):
   - Nabije oog: glans w op (29,24) aan de lichtkant, pupil K (30,24), iris y (31,24), gekleurde reflectie a op (30,25) (was rood r).
   - Verre oog: lid d op (24,23) (was r).
   - Snavel: donkere haakpunt d op (23,26), bleke b op (24,26).
   - Op 10× bekeken: vlak donker lid, gouden iris met pupil en glans links. Dat oogt trots en rustig, niet boos (geen zwart lid tegen de kroon) en niet lief (geen ronde iris met witte vlek).
2. **Banding rechterflank** (22 px): de strook lijfbasis m tussen buikschaduw a en lijfschaduw d is op rij 36–44 versmald tot 1 px en verdwijnt vanaf rij 45. De overgang is nu a → m (1 px, uitlopend) → d. Vier evenwijdige banden zijn het niet meer.
3. **Hooglicht romp linksboven** (10 px, alleen m → l): een kleine schouderzone (24–25,29), (23–25,30), (22–24,31), (22–23,32), aansluitend op de lichte rand die er al was.
4. **Stafpunt zichtbaar** (12 px):
   - Omlijning d op (13,18)–(13,21) en K op (16,18)–(16,19) rechts.
   - De zwarte stray (17,19) is weer kroontint o.
   - De punt zelf is lichtgoud y links (rij 18–20) en donkergoud a rechts en onderaan, in plaats van de basistint.
5. **Opschonen** (12 px):
   - De klont onder de hand: (15,46) K → d; (15,47) is K gebleven (het L-vormige randje is geen 2×2 meer).
   - De kroononderrand rechts (40–42,22) r → K en het losse rood (45,22) → K; daarmee is rij 22 van x34 t/m 46 één doorlopende rand.
   - De drup (40–42,23) en (42,24) is weg (silhouet −4).
   - In de hand is één van de twee diagonale penscheidingen weg ((14,43), (15,44), (16,45) d → m), zodat er één doorlopende scheiding overblijft.

## Diff per zone t.o.v. ronde 12 (`controle13_uitvoer.txt`)
| Zone | px |
|---|---|
| 1 ogen en snavel (x23–31, y23–26) | 6 |
| 2 flank (x29–35, y36–50) | 22 |
| 3 romp linksboven (x21–27, y28–33) | 10 |
| 4 stafpunt (x13–17, y18–21) | 12 |
| 5 klont (15,46–47) | 1 |
| 5 kroononderrand + drup (x40–46, y22–24) | 8 |
| 5 hand (x12–20, y41–45) | 3 |
| **buiten de genoemde plekken** | **0** |
- Totaal 62 px; silhouet −4 (de drup), +0; 1629 → 1625.
- Controle: palet identiek; **0 open randen**; geen 2×2-klonten zwart; 15 kleuren + transparant; aandeel zwart 0,12.

## Zelf gekeken (4×, 1×, 10× naast ronde 12)
- Op 4× en 1× zie je de staf nu met een duidelijke punt. De flank is rustiger (geen streepbanden), de romp heeft een lichte schouder, en onder de kroon rechts loopt de rand recht door zonder drup.

## Eerlijk: wat nog niet klopt
- **Kroonpatroon bij de stafpunt:** de punt ligt over de gouden boogvlek van de veer linksboven (14–15,18–19). Die vlek is nu deel van de stafpunt, dus die ene veer mist zijn eigen vlek (de andere 8 zijn identiek). Dat was niet te vermijden met de punt op deze plek; Jordi kan kiezen of de punt 1–2 px korter moet.
- **Ogen en snavel op 1×:** beter dan ronde 12 (er is nu een glans aan de lichtkant, een lid op het verre oog en een donkere haakpunt), maar binnen de huidige kopmaat blijven het kleine puntjes. De echte oplossing (een grotere kop) is een silhouetkeuze voor Jordi.
- **Flank:** de 1 px brede m-lijn stopt op rij 44. Op 8× zie je dat het einde abrupt is in plaats van geleidelijk.
- **Hand:** met één penscheiding leest hij rustiger, maar nog steeds als een vuist.
- Niet aangeraakt (zoals gevraagd): kroonomtrek rechtsboven, vleugelpunt, kopmaat, palet, poten.

## Lessen
- Bij een script dat zijn eigen bronbestand herschrijft: eerst lezen, dan openen om te schrijven (`open(src,'w')` maakt het bestand leeg vóór het lezen; het raster is daarna opnieuw opgebouwd uit ronde12).
