# Potoo eind_r3: rechterrand vleugel minder kaarsrecht (7 nov)

Opdracht (Jordi, over "de rechterrand van de vleugel (x45, y31–48) is een kaarsrechte lijn van 18 px"): "ja die mag wat minder kaarsrecht nog".
Zone x40–47, y28–50. Start `eind_r2/potoo.png`, palet ongewijzigd.

## Wat
- `wijzig.py`: 40 indexwissels, elk met controle op de oude waarde (0 afwijkend). Diff buiten de zone: 0.
- Rechterrand per rij, r2 → r3: y28–29 45, y30–31 46, **y32–37 47** (top van de bolling), y38–42 46, y43–46 45, y47–48 44 (sluit aan op de staart, x44 vanaf y49).
  Trappen 2-2-6-5-4: oplopend naar de top, daaronder afnemend (bolle curve), dan de verticale staartrand. Het oude losse uitsteeksel op y30 (x46) zit nu in de curve.
- Modelmeting (rechterrand model per spriterij): y30–31 46,9, y34–37 46,2, y38–48 45,5. De bolling op x47 ligt ±1 px buiten het model (toegestaan: "een paar px naar buiten, alleen voor deze curve"); het model zelf is daar ook vrij recht, alleen met de bult op y30–37.
- Buitenlijn 1 px zwart (index 1). Sikkelschaduw (5) schuift mee: x46 y32–37 → x45 y38–42 → x44 y44–46 → x43 y47–48; erbinnen 6. De oude 5-strook op x44 y36–40 is 6 geworden (geen dubbele band). Donkere inkeping 4/3 op x43–44 y41–44 ongewijzigd.

## Controle (`controle.py` → `controle.txt`)
- Gewijzigd 40 px, buiten zone 0, palet gelijk, 12 kleuren (gelijk).
- Open randen: 56 vóór en na, 0 in de zone (alle in de zone zwart).
- Clusters < 3 px: 148 → 147; in de zone geen nieuwe (het losse 4-pixel op 44,48 is weg). Zwarte "clusters" van 1–2 px zijn diagonale lijnstukken.

## Zwakke punten (eerlijk)
- De staartrand x44 y47–57 is nu 11 px recht (was 9); buiten de zone niet aan te passen, model is daar ook recht.
- Bolling 1 px voorbij de modelomtrek op y32–37.

`vel.png`: eind_r2 8× | eind_r3 8× | model 8×, daaronder 1× licht/donker (`vel.py`).
