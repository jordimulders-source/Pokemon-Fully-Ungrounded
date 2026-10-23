# Alpaca fase 1, ronde 14: evolutiehints op ronde 13

Jordi over ronde 13: "veel beter". Het nabije (rechter) oog blijft precies zoals het is, met glans. Het verre oog is niet zichtbaar; het zwarte stukje boven op de neus blijft als zwarte streep. Verder niets aan het ontwerp veranderen.

Ronde 14 is daarom ronde 13, pixel voor pixel, plus per variant precies één kleine hint naar de evoluties (`docs/concept/ontwerp/alpaca/ONTWERP.md`: kuif → bombín, oorwol → vlechten, halswol → kragen/manta). Geen nieuwe kleuren: alle hints gebruiken het palet van ronde 13. Ogen, neus, kop, nek, lijf, poten en vuisten zijn onaangeraakt. In frame 2 zakken de kophints mee met de kop (1 px), de halshint blijft staan, net als de hals in ronde 13.

## De varianten (coördinaten = frame 1, x/y vanaf 0)
| Variant | Hint | Pixels | Gewijzigd |
|---|---|---|---|
| **A** bombín-zaadje | Smal randje onder de pompon: de bol van de pompon lijkt op een rand te staan, zoals een bolhoedje in wording. Het silhouet blijft gelijk, dus het leest als wol en niet als hoed. | rij 9, x21–28: `u v v v v v v u` (oudroze, mauve aan de uiteinden). Rij 10 eronder had al crème hooglicht en werkt nu als lichte 'rand'. | 7 px |
| **B** vlechtpuntjes | Onder elk oor hangt een smal wolplukje langs de kop, met een eigen omlijning (de kopomtrek blijft erachter staan), zodat het als kwastje leest en niet als bolle wang. Voorbode van de vlechten van fase 3. | verre oor: x16 y9 `V`, x15–16 y10 `VW`, x15–16 y11 `Vw`, x16 y12 `K`. Nabije oor: x33–35 y10 `VwK`, x34–35 y11 `wK`, x35 y12 `K`. | 12 px (+12 oppervlak) |
| **C** aguayo-streepje | Hetzelfde weefsel als de manchet (magenta, geel, turquoise), 4 px in de hals; het rechter pixel in schaduw-magenta zodat het om de hals draait. Eronder 3 px oudroze: het streepje ligt in de wol, geen sticker. Voorbode van de kragen (fase 2) en de manta met zigzagband (fase 3). | x24–27 y26 `M Y T s`, x24–26 y27 `v v v`. | 7 px |
| **D** | A + B + C samen. | zie boven | 26 px |

Controle (`bron/bouw14.py`): geen open randen in frame 1 en 2 van alle varianten; 16 kleuren, index 0 transparant; `anim_front.png` 64×128. Oppervlak: A en C 923 (gelijk aan ronde 13), B en D 935.

## Checklist (§0)
Ongewijzigd ten opzichte van ronde 13 (zie daar); de hints raken geen enkel punt. Punt 2: de plukjes van B zijn aan de oorbasis vastgemaakt, geen losse stukjes. Punt 3: B breekt de rechte zijkant onder het verre oor (x17, y8–13) een beetje.

## Eigen voorkeur
**C**, en eventueel **C + B**. C is de enige hint die op 1× echt zichtbaar is en hij verbindt de kop met de vuisten: hetzelfde weefsel op twee plekken leest als een vachttekening, niet als accessoire. B is heel subtiel maar klopt (de oorwol hangt al een beetje). A is op 1× nauwelijks te zien; dat is binnen de opdracht ("leest niet als hoed"), maar het zaadje van de bombín komt pas echt tot zijn recht in fase 2 (koepel met randje). D is iets druk rond de kop, maar nog steeds dezelfde alpaca.

## Bestanden
- `variant_A/` … `variant_D/`: `anim_front.png`, `normal.pal`
- `compare.png`: ronde 13 en A–D op wit en gevechtsgrond (1× en 3×), plus 4×-uitsnede van kop en hals.
- `bron/`: `palet.txt` en `r13_f1.txt`/`r13_f2.txt` (kopie van ronde 13), `bouw14.py` (hints en controle), `vergelijk14.py`, `variant_X_f1.txt`. Vanuit de repo-root:
  - `python3 docs/concept/sprites/alpaca/ronde14/bron/bouw14.py`
  - `python3 docs/concept/sprites/alpaca/ronde14/bron/vergelijk14.py`

## Lessen
- **Hints op een goedgekeurde sprite als overlay op het raster** (rijen 'y x pixels' bovenop een kopie van het goedgekeurde raster) garanderen dat de rest letterlijk blijft staan, en laten per variant het aantal gewijzigde pixels zien.
- **Een plukje naast de kop heeft een eigen omlijning nodig:** de eerste versie van B haalde de kopomtrek weg en las als bolle wang; met de kopomtrek erachter en een eigen randje leest het als een los kwastje.
- **Een felgekleurd streepje in vacht leest als sticker** tot het schaduw krijgt: één rij schaduwkleur eronder en de buitenste pixel in de schaduwvariant laten het in de wol liggen.
- **Frame 2 meenemen:** kophints moeten met de kop meezakken (y ≤ 22 → +1), halshints niet; controleer open randen in beide frames.
