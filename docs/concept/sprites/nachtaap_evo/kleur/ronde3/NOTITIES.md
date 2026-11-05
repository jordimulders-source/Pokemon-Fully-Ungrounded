# Nachtaap fase 2: kleursprite ronde 3

In deze ronde is alleen het middenstuk van de maan veranderd, in de zone x 4–24, y 36–46. Al het andere is ronde 2 en bevroren.

**Wat er veranderde (7 px, budget ±25):**
- **y 41, x 13:** violet → wit. De wig die tot y 41 omhoog liep, is daarmee weg.
- **y 42, x 12–14:** `l b b` → `n b n`. Het middenstuk is nu een kleine ronde bult: 1 px boven de bovenrand van de ogen, met zilverlila als overgang.
- **y 43–46, x 12:** `l` → `b`. Het lichte randje langs het middenstuk las als het begin van een middenstreep; dat is nu gewoon vacht.

**Nagemeten tegen de onderlaag** (4:1 verkleind, `bron/diff_uitvoer.txt`):

| | dikte maan in het midden (x 12 / 13 / 14) | maanpixels (w + n) | overlap met onderlaag |
|---|---|---|---|
| onderlaag | 5 / 5 / 6 | – | – |
| ronde 2 | 4 / 4 / 5 | 94 | 52 |
| ronde 3 | 5 / 5 / 6 | 97 | 55 |

In ronde 3 is de maan bovenaan één doorlopende dikke boog. De ronde buitenrand is niet aangeraakt.

**Bewijs:**
- diff buiten de zone t.o.v. ronde 2: 0, met hetzelfde palet;
- alpha-diff: 0 (1459 px, zowel tegen de `.txt` als tegen de `.npy`);
- open randen: 0.

**Vel:** de kop op 8× (ronde 2 | ronde 3 | onderlaag), en de sprite op 4×, 3× en 1× op licht en op donker.

## Lessen
- **Een middenstuk dat met een lichte rand (`l`) doorloopt tot ver tussen de ogen, leest als een wig of middenstreep.** Dat is het gezicht van fase 1. Een bult van 1 rij boven de ooglijn, met de schaduwtint van de maan als afronding, leest als "inbollen".
- **Meet de dikte van een vlak per kolom tegen de onderlaag** (hier x 12–14), niet alleen het totaal aan pixels.
