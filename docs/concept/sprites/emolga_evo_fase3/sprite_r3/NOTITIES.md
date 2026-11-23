# Fruitvampier – sprite r3 (zelfde maker als r2)

Start: `sprite_r2/A0.png`, `A.png` en `A_geel.png`. Reparaties 1–8 van de keurder (`keuring_r2/KEURING.md`) zijn als bovenlaag per
pixel toegepast in `gereedschap/bouw_r3.py`. Elke pixel staat daar met zijn oude kleur, en het script stopt als die oude kleur niet klopt.
Bewijs: `gereedschap/controle_r3.py`. De diff t.o.v. r2 bestaat precies uit de benoemde pixels; buiten de zones is hij **0** voor alle drie de bestanden.
Vel: `gereedschap/vel_r3.py` → `vel.png` (r3 A0 | r2 A0 | r3 A | r2 A | r3 A_geel | model verkleind, 8×, met 1× licht/donker en 2×).
Palet ongewijzigd, 13–14 kleuren gebruikt, 64×64, index 0 transparant.

| # | zone | px | wat |
|---|---|---|---|
| 1 | onderste vleugelvlak | 34 | D → E: bolling links van de vouw, taps naar onder. Rij 24 x32–34 · 25–26 x31–34 · 27 x29–34 · 28 x28–33 · 29 x29–33 · 30 x30–32 · 31 x31–32 · 32 x32. Sluit aan op het E-vlak erboven. D blijft 1–3 px langs de vouw, langs de gele rand rechts en onderaan bij de kop. Vouwlijn en geel zijn niet aangeraakt. |
| 2 | open rand | 1 | (38,41) Y → K. Model: dekking x38 90 %, x39 20 %, dus het silhouet eindigt op x38 en die pixel wordt zelf lijn. Silhouet gelijk. |
| 3 | lichtkant | 1 | (21,18) K → D |
| 4 | kin | 9 | B → W: (28–29,31), (27–30,32), (26,33), (25,34), (25,35). B blijft rechts (30–32) en onderaan (rij 36). |
| 5 | borstvlakje | 6 | W → B: rechter- en onderrand (31,9), (31,10), (30,11), (30,12), (29,13), (27,14). Linksboven blijft wit. |
| 6 | vuisten | 3 | (30,0) en (34,0) worden transparant: model 65 % en 66 %, en de fijne meting toont een gat op x30,5 en x34. (33,0) D → K als rechterrand van de rechtervuist. Twee vuisten: x28–29 en x31–33. Silhouet −2 px. |
| 7 | A0: voorhoofdgeel | 1 | (24,49) W → L. Model 35 %, de hoogste dekking na de bestaande 4 px. |
| 8 | A/A_geel: kap | 1 | (24,50) E → D |

Niet 1-op-1 uit het model: de tintverdeling binnen de vlakken (1, 4, 5), want het model is daar egaal of anders belicht. (33,0) is K als randlijn.

## Zwakke punten
- **V-kap:** blijft klein. Dat is een ontwerpvraag (de kruin is in het model 3 rijen hoog), geen spritefout volgens de keurder.
- **Diagonale B-rand:** de rand van het borstvlakje is een diagonale reeks van 1 px. Het werkt als selout, maar het zijn losse 1-px-trapjes.
- **Keurder punt 9:** A heeft geen voorhoofdgeel (kap ligt erover). Dit blijft een keuze voor Jordi; `A_geel` is de variant met geel.
