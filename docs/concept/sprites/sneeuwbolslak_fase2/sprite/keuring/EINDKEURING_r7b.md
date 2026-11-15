# Eindkeuring r7b – sneeuwbolslak fase 2

Getoetst: `sprite/maker/r7b.png` / `raster_r7b.txt` / `pal6.py` (via `r7b_bouw.py`) tegen het model `sprite/r8_bol_r7.png`. Gemeten met `meet/px.py` (modeltint per spritepixel), `recht.py`, `bewaak.py` en een telling van de tintvlakjes. Daarnaast gelegd: Glalie, Regice en fase 1. EINDKEURING_r6 pas gelezen na de eigen blinde indruk.

**Oordeel: PASS na de MOET hieronder** (8 px, alleen in de bol, per script toe te passen).

## Eerste indruk (blind, 8× en 1×)
- Op 1× leest de sprite als het model: kop met oog en blauwe wang, de ronde bol met barst en ijspunten, de rode ring, de flap en de staart in scherven.
- De bol leest nu als **glas met iets erin**: donkere buitenlijn, lichte glasrand binnenin (ook aan de schaduwkant), een glanslicht linksboven met `w`-kern, en daarbinnen een middentint `b` met witte, krullende banen en losse vlokken. Dat is een sneeuwstorm, niet meer een bevroren bal. Jordi's punt "je ziet niet meer wat er binnenin gebeurt" is opgelost.
- De barst is `d` (geen zwart meer) en volgt het pad van het model: stam (36,25)–(34,29), linkertak tot (30,33), rechtertak tot (37,37). Steekproef `px.py`: model-L 75–130 op die pixels, dus klopt.
- Rond: de zijkanten zijn 4 px verticaal (x 21 en x 42, y 29–32); bij een cirkel met straal 10,6 hoort ±7 px vlak, dus dat is rond. Silhouet-diff 0, 21 rechte stukken (langste 5 px, niet in de bol). Buiten de bol diff 0 ten opzichte van r6.
- Totale helderheid van de binnenschijf gelijk aan het model (gem. L 187 tegen 188).

## Trouw aan het model (bol)
- Het model toont de storm als donkere banen op een lichte doorkijk; r7b draait dat om (witte banen op `b`). Dat is een stilering, geen herontwerp: dezelfde plekken, dezelfde gemiddelde toon, en het is precies wat Jordi vroeg (zichtbare storm). Akkoord.
- **Wel een gemiste modelvorm: de heldere bodem.** Het model is op y 37–38, x 24–33 duidelijk licht (`e`, L 200–230): de kaustiek onderin het glas. r7b heeft daar op y 38 `b` (x 28–35). Alleen de buitenste rij (y 39) is licht, waardoor de bodem van het glas als dunne rand leest en de bol onderaan donkerder oogt dan het model. Zie MOET.

## MOET (exact, letters uit `raster_r7b.txt` gecontroleerd)
| Pixel | Nu | Wordt |
|---|---|---|
| (27,38) | c | e |
| (28,38) | b | e |
| (29,38) | b | e |
| (30,38) | b | e |
| (31,38) | b | e |
| (32,38) | b | c |
| (33,38) | b | c |
| (33,34) | b | e |

- y 38: de lichte bodem van het model (glas leest door licht onderin).
- (33,34): de lichte kern van het model (x 31–35, y 31–35) staat nu als dambord `e b e` op y 34 (x 32–34); dicht maken tot één vorm.
- Gecontroleerd in een proefrender: geen nieuwe tinten, silhouet onveranderd, de storm blijft leesbaar.

## MAG
- De stormbanen zijn 1 px diagonalen; als 4-verbonden vlakjes tellen ze als veel spikkels, maar 8-verbonden zijn het doorlopende bogen. Laten zo.
- Baan B (linksonder) loopt vrij evenwijdig aan de glasrand; één onderbreking (bijv. (25,33) `e`→`b`) maakt hem minder ringvormig. Niet nodig.
- Drie `w`-vlokken op één rij (32,33), (35,33), (38,33): eventueel één een rij verschuiven voor meer chaos.

## Ter info voor Jordi
- De storm is gestileerd als witte wervel op een blauwe doorkijk (in het model donkere banen op licht). Op 64 px is dat de manier om de storm op 1× te zien; plek, barst en ronding zijn die van het model.
