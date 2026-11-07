# Lama fase 3: kleur ronde 5A5 (5 nov)

**Jordi over 5A4 (letterlijk):** "aan de linkerkant is de kleur van de bombin vervallen naar bruin en loopt die pixels te ver door. aan de rechterkant vind ik hem goed. Nu de beschaduwde achterpoot nog, dat is gewoon 1 effen kleur vlak, dat kan niet".

Gemaakt vanaf `ronde5A4/ronde5A4.txt`, met de hand in `bron/wijzigingen.txt`.
- **39 px gewijzigd:** bombín links 10, verre achterpoot 29, **elders 0** (`controle.txt`). Oog en rechterkant van de hoed: 0 px.
- Alpha alleen −2 (x16–17 y13, de ingekorte rand). 0 open randen, 15 kleuren.

## Bombín links
- **Glans in hoedtinten:** koel donker `D` (x21–22 y8, x20 y9), zoals de lichtjes in de vlecht, in plaats van beige/bruin `S`/`d`.
- **Rest zwart:** x23 y8, x21 y9 en x20 y10 zijn `k`.
- **Rand 2 px korter:** begint nu op x18 in plaats van x16, helemaal zwart (de bruine `dd` op x18–19 is weg).

## Verre achterpoot (x33–40, y47–58), omtrek ongewijzigd
| rij | wat |
|---|---|
| y47 | schaduwsikkel `dddd` onder de rok (dij-ronding) |
| y48–56 | lichtkant: smalle kolom `C` links (x33–34 bij de dij, daarna x34); basis `S`; schaduwkant `d` rechts (x40) |
| y52 | hak zacht aangegeven met `d` (x39) |
| y57–58 | hoef donker: `ddSdd` met lichtje `S` (x36 y57), daaronder `dkkk` |

- De scheidingslijn met de nabije poot blijft `d` (omlijningsbasis, x41).
- De poot blijft donkerder dan de nabije: alleen `C`/`S`/`d`, de nabije heeft `H`/`C`/`S`.

## Eerlijk
- Schaduwkant en scheidingslijn liggen naast elkaar (`dd`, x40–41). Op 1× is dat een donkere rand tussen de achterpoten.
- De lichte kolom `C` maakt de dij bovenaan vrij licht. De poot leest nu als cilinder, maar Jordi kan hem iets donkerder willen.

## Bestanden
- `ronde5A5.txt`, `lama3.png`, `normal.pal`, `controle.txt`.
- `vel_ronde5A5.png`: 4× licht/donker, 1× (5A5 en 5A4), kop 8× 5A4|5A5, achterpoten 8× 5A4|5A5.
- `bron/wijzigingen.txt`, `bron/bouw.py`, `bron/vel.py`.
