# Kudu sprite ronde 5b (maker)
Besluiten van Claude op de vragen uit r5:
1. **Hals:** de meting wint, dus de vachtstrook is 2 px breed zoals in het model.
2. **Onderrand van het oor (rij 22, x2-5):** schaduwkant, blijft zwart.

Verder is niets veranderd.

**Script:** `sprite/r5b.py` (= `r5.py` + één stap `hals2`). Oog wisselen gaat met `python3 r5b.py A|B|C|D`; B staat in `kudu_r5b.png`, A/C/D in `kudu_r5b_oog{A,C,D}.png` (+ 8x).

## Gewijzigde pixels t.o.v. r5 (9 px, alle m/l → M)
Regel: elke cel in het halskanaal (x12-16, rij 28-38) met ≥ 75% modelvacht wordt M.

| Pixels | Modelvacht |
|---|---|
| (14,28)–(14,34) | 100% (tweede kolom naast de r5-lijn op x13) |
| (15,36) | 79% (naast (14,36)) |
| (12,29) | 91% (onder de kaak, sluit aan op (13,29)) |

De strook is nu 2 px breed:
- x13-14 van rij 28 tot 34;
- x14-15 op rij 36;
- 1 px op rij 35, 37 en 38, omdat de tweede kolom daar in het model < 75% vacht heeft.

## Pixels
- T.o.v. de kale reductie van model A3: 607 van 1362 (vacht 211, manen 151, staal 137, lijn 83, oog 11, donker 11, roze 3).
- T.o.v. r4: 171.
- Per pixel staat alles in `wijzigingen.txt` (stap `hals2`).
