# Lama fase 3: kleur ronde 5A3 (5 nov)

**Jordi over 5A2 (letterlijk):** "zet de hoed maar wat verder naar onderen en maak hem 1.2x zo groot zodat die op de vlechten aansluit. Daarnaast is het oog nu veel slechter. Je zat eerst met het oog best ok, maar hij leek nog wat bozer dan echt nonchalant".

Gemaakt vanaf `ronde5A2/ronde5A2.txt`, met de hand in `bron/wijzigingen.txt`.
- **52 px gewijzigd:** hoed/kop y0–13: 44, oog: 8. **Elders 0** (`controle.txt`).
- 0 open randen, 15 kleuren, palet ongewijzigd.

## Bombín (±1,2× en 1 rij lager)
| onderdeel | 5A2 | 5A3 |
|---|---|---|
| bol | y5–9, max. 7 breed | y6–10 (x22–24 / x20–26 / x19–26), max. 8 breed, glans `SSd` linksboven |
| band | y10, 6 px | y11 `RRrrrrm`, 7 px (x20–26) |
| rand | y11, 11 px | y12, 14 px (x16–29), glans `dd` op x18–19 |

- **Aansluiting op de vlechten:** rechts zakt de rand naar y13 (x24–30) en sluit daar aan op de bovenkant van de vlecht (y14, x27–29).
- **Oren blijven zichtbaar:** het linkeroor op y1–6 (x19–21), het rechteroor op y1–10 (punt en buitenkant x27–29).
- **Kop eronder:** de oude kruinrij (y12) zit nu onder de rand. De pony is op y13 nog zichtbaar links van de rand (x19–23, `dHHCS`).
- **Buiten silhouet_A: +9:**
  - rand links x16–19 y12;
  - rand rechts x28–29 y12, x28–30 y13.
- **Silhouetpixels leeg: 2:** x22 y5 (de oude bovenkant van de bol; de hoed staat lager) en x18 y11 (de oude rand).

## Oog
- **Terug naar 5A, exact.** Daarna 3 px tegen het boze: het lidvlak boven de lidlijn is een tint lichter.
  - x22 y14 `d` → `S` (de donkerste pixel boven het lid);
  - x23 y14 `S` → `C`;
  - x24 y14 `S` → `C`.
- Lidlijn, oogwit, pupil en kring zijn de pixels van 5A. De scheiding met de vlecht (x26 `S`) is gebleven.

## Vlechten
Zoals 5A2 (zwart met koele lichtjes); ze sluiten bovenaan op de hoedrand aan.

## Eerlijk
- De rand is links lang (x16–29). Op 4× oogt hij als een brede hoedrand; Jordi kan hem links 1 px korter willen.
- Het verschil in het oog is klein (3 px, zoals gevraagd). Of het nu nonchalant genoeg is, moet Jordi beoordelen.

## Bestanden
- `ronde5A3.txt`, `lama3.png`, `normal.pal`, `controle.txt`.
- `vel_ronde5A3.png`: 4× licht/donker, 1× (5A3 en 5A2), kop 8× (5A | 5A2 | 5A3 | render), oog 12× van 5A en 5A3 naast de oogstudie.
- `bron/wijzigingen.txt`, `bron/bouw.py`, `bron/vel.py`.
