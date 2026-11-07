# Lama fase 3: kleur ronde 5A4 (5 nov)

**Jordi over 5A3 (letterlijk):** "hoed mag 1 pixel naar beneden, want nu lijken de vlechten juist uitgebreid. Ogen ben ik tevreden mee nu". Het oog is daarmee bevroren.

Gemaakt vanaf `ronde5A3/ronde5A3.txt` met `bron/schuif.py`: de hoedcellen staan er met de hand opgesomd, net als de vulling van de vrijgekomen cellen.
- **47 px gewijzigd, alle in y6–14.** Oog (x22–26 y14–18) en de rest: **0 px diff** (`controle.txt`).
- 0 open randen, 15 kleuren.

## Bombín exact 1 rij omlaag
- **Nieuwe plaats:** bol y7–11, band y12, rand y13 (x16–29). Het zakkende rechterdeel ligt nu op y14, x27–30.
- **Oog en vlecht:** op y14 landt het rechterdeel alleen op x27–30, want x24–26 is het bevroren oog. De vlecht begint nu onder de rand (y15) en steekt er niet meer boven uit. Het lichtje bovenaan de vlecht (x28 y14) zit nu onder de rand.

## Vrijgekomen cellen, met de hand gevuld
| cel | nu | reden |
|---|---|---|
| y6 x22–24, y7 x25 | leeg | tussen de oren |
| y7 x20–21 | `C k` | linkeroor |
| y7 x26 | `d` | rechteroor, binnenrand |
| y8 x19 | `d` | linkeroor |
| y12 x16–18, x29 en y13 x30 | leeg | oude rand, buiten het silhouet |
| y12 x27–28 | `k k` | oorvoet onder de rand |

- **1 extra px:** y11 x27 `k` → `C` (rechteroor). Het oor loopt door op de plek waar de hoed nu lager zit.
- **Oorpunten zichtbaar:** links y1–8, rechts y1–11.
- **Silhouet_A:** buiten +8 (rand: x19 y12, x28 y12, x16–18 y13, x28–29 y13, x30 y14); leeg −6 (x22 y5, x22–24 y6, x25 y7, x18 y11; tussen de oren boven de lagere hoed).
- **De pony** zit nu volledig onder de rand; de kop begint op y14 direct onder de rand.

## Bestanden
- `ronde5A4.txt`, `lama3.png`, `normal.pal`, `controle.txt`.
- `vel_ronde5A4.png`: 4× licht/donker, 1× (5A4 en 5A3), kop 8× (5A3 | 5A4 | render).
- `bron/schuif.py`, `bron/vel.py`.
