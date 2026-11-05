# Lama fase 3: kleur ronde 4 (5 nov)

**Jordi over ronde 3 (letterlijk):**
- "je luistert niet naar wat ik zeg, probeer het hoofd na te maken zoals in het model, nu ben je gewoon weer dingen aan het verzinnen"
- "het model is goed, probeer dat zoveel mogelijk na te maken, als we het hoofd moeten opschalen dan doe je dat nav het model"

**Aanvulling (letterlijk):** "houd er wel rekening mee dat de vlecht en het oog dicht bij elkaar zitten, dus probeer dat goed uit te werken".

## Werkwijze
De kopzone (x8–35, y0–25) is **overgetrokken** van `kleur/kopbron/` (model, kop 1,25× om de oorpunten), niet getekend.
- Per cel gelden het onderdeel uit `kop_labels.txt` en de kleurfamilie uit `kop_kleur_64.png`.
- Een lijn komt alleen waar `kop_lijnen.txt` `#` heeft: `d` aan de lichtkant (links/boven), `k` aan de schaduwkant.
- Toegevoegd is alleen licht en schaduw binnen elk onderdeel, in het palet van 2b:
  - crème `H`/`C`/`S`;
  - hoed `k` met glans `S`/`d`;
  - band `RRrrrm`;
  - vlecht `d`/`S`/`k`.
- Handwerk in `bron/kop.txt`. `=` betekent: pixel van 2b houden (labels `x` en leeg onder de kop). `bron/bouw.py` plaatst en controleert.

## Controles
- **Buiten de kopzone 0 px diff met 2b.** In de kopzone 232 px gewijzigd.
- **Diff kop vs. bron (`diff_bron.txt`):** onderdeel wijkt af in **0 cellen**: leeg/gevuld en kleurfamilie per label kloppen overal.
- Buiten `silhouet/ronde2.txt`: +41 px. 19 silhouetpixels zijn leeg, omdat kop en oren nu de vorm van de bron volgen.
- 0 open randen, 15 kleuren.

## Afwijkingen van de bron (±1 px, met reden)
| x,y | bron | sprite | reden |
|---|---|---|---|
| x26 y2, x27 y3, x28 y7 | oorvulling aan de rand | `k` | open rand (oor van 2 px tegen transparant), schaduwkant |
| x26 y3, x19 y5, x19 y6, x19 y13 | vulling aan de rand | `d` | open rand, lichtkant |
| x26 y15, x26 y17 | lijn (hals/oog) | `S` | 1 px kopkleur tussen de oogring en de vlecht, zodat oog en vlecht op 1× los lezen (Jordi's aanvulling) |
| x20–25 y11 | hoedband `B`, bemonsterd donker | `RRrrrm` | het onderdeel is de band; rood zodat hij leest (de band valt in het model tussen twee rijen) |
| x15–18 y25 | label `x` met lijn `#` | `k` | onderrand van de onderlip, valt over de halsband; de kop wint (regel 4) |
| x14 y25 | `V` | `k` | puntje van de nabije vlecht, zoals in de bron |

## Oog en vlecht (aanvulling Jordi)
- **Oog zoals in het model:**
  - zwarte ring `k`: x24 y15–17, x25 y17–18, x26 y16;
  - met het lid `S` erin: x25 y15–16.
- **Vlecht erachter in warm bruin:**
  - linkerrand `d` (x27 y15–17, x26 y18–20), lichtjes `S` (x28 y16, x27 y18, x28 y20), donkere knotten en de buitenrand in `k`;
  - zo heeft hij een andere tint dan de zwarte oogring;
  - knotten wisselen licht en donker af langs achterkop en hals (y15–25).
- **Scheiding:** x26 y15 en x26 y17 zijn kopkleur `S`. Op y16 raken ring en vlecht elkaar wel: de bron laat daar geen ruimte, en de scheiding is dan zwart tegen bruin.

## Bewust niet gedaan
- **De tullma en de gouden ring** zitten niet in `kop_labels.txt` binnen de kopzone, dus die zijn niet getekend. De rode tullma van 2b (y21–22) is daardoor vervangen door de vlecht van de bron.

## Eerlijke zwakke punten
1. **Het oog is op 1× klein:** een ring van ±3×4 px met lid. Dat is het model zoals het staat; ik heb het niet vergroot.
2. **Op y16 raken oog en vlecht elkaar** (zwart tegen bruin, geen crème ertussen), omdat de bron daar geen ruimte laat.
3. **Er is geen tullma meer zichtbaar,** omdat die buiten de bron valt.

## Bestanden
- `ronde4.txt`, `lama3.png`, `normal.pal`, `diff_bron.txt`.
- `vel_ronde4.png`: zelfde opbouw; kop 8× met overtrekvel-render | `kop_kleur_64` | ronde 4.
- `bron/`: `kop.txt`, `bouw.py`, `vel.py`.

## Lessen
- Trek de kop over van een bemonsterde modelbron (labels + lijnen + kleur per cel) en tel de onderdeel-diff tegen de labels (doel 0). Zelf tekenen leidt tot verzinnen.
