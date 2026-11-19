# Palpaca r2 (19 nov): benoemde reparaties op r1, allemaal naar het model

Zelfde keten als r1 (`scripts/alles.sh`). Vel: r2 8× | r1 8× | model 8×, 1× op licht/donker (+ oude sprite en r1 op 1×), close-ups kop en poten 12× naast het model.

## Opdracht (Claude) en Jordi's correctie
1. Kop/gezicht. **Jordi:** "dat de kop hoekig leest moet je oplossen met kleurgebruik en schaduwen". Het silhouet van de kop is dus NIET aangepast.
2. Verre achterpoot neutraal grijsbeige in plaats van paarsroze.
3. Bobbelige krulrand op rug, bil en staartpluim waar het model die heeft.
4. Hals lichter en neutraler.

## Wat er veranderd is
- **Oog**: model natief x 46–50, y 30–37 = 2,1 × 3,4 spritepx → nu 2×4 (was 2×3). Glans linksboven (natief 47,30–33), lichtere onderkant in 6 (natief 47–49,36), onderrand dicht. Verre oog op de wangrand blijft.
- **Kuif (alleen tinten)**: de krullijn van het model (natief 32–36,28 → 38–42,30 → 43–46,29–26 → 47–51,25–28) staat er nu als twee boogjes in 5. Het boogje direct boven het oog is 4, zodat het oog vrij blijft. De modelschaduw onder de kuif (toon 193–211) is 4 en volgt de boogjes (1 px erboven) in plaats van een rechte band. Het hooglicht linksboven op de kuif blijft.
- **Ronde kop via schaduw**: sikkel in 4 langs de rechterrand. Die is 1 px van rij 10 tot 13 en groeit naar 2–3 px van rij 14 tot 18 (model 190–213). Zachte wanglijn in 4 rechts van het oog (natief 52–55,29–44, doorlopend in het model) maakt het gezicht rond; onderaan gaat hij op in de sikkel.
- **Snuit**: neusgat (2,15), mondlijn (2,17)(3,17), kin (4,18) en opkrul (5,17), naar het model (natief 33–39,42–44).
- **Verre achterpoot**: paletindex 11 = 172,154,134 (basis; model 154,138,114 iets warmer zoals de rest van het palet). Index 15 = 124,108,94 (schaduw waar de poot achter het lijf verdwijnt; model 125,110,91). Het oude 15 (paars, alleen in het oog) is vervangen door 6 in het oog. Kraag en manchetten gebruiken alleen 12/13/14 (magenta 11 werd al niet gebruikt).
- **Hals**: gemeten 184–195 onder de kin → 3; alleen de kinschaduw (167–179) is 4.
- **Krulbultjes**: vakken met 28–45 % model en ≤ 2 figuurburen op de wolrand. Overgenomen: rugkrul (19,23)(20,23), staartpluim (24,20)(26,19)(29,20), bil (28,31). Niet aan de kop (Jordi). Niet de rechte hals- en kaakrand, niet de poten. Borst en voorkant van het lijf hebben in het model geen bultje dat meetelt. Knie (0,35) liet ik weg: dat werd een los 1-px stekeltje. Een bultje aan de bovenkant krijgt selout 6.

## Afwijking van de onderlaag (`meet.py`)
Silhouet t.o.v. de r2-onderlaag: **0 px**. De onderlaag bevat nu de 6 bultjes.

| zone | px | opschonen | reparatie | totaal |
|---|---|---|---|---|
| kop + gezicht | 242 | 71 | 26 | 80 |
| hals + lijf | 281 | 38 | 5 | 43 |
| handschoenen + manchetten | 84 | 32 | 6 | 38 |
| poten (licht) | 102 | 20 | 0 | 20 |
| staart | 62 | 17 | 1 | 18 |
| oren + kwastjes | 27 | 10 | 0 | 10 |
| verre achterpoot | 42 | 8 | 0 | 8 |
| kraag | 9 | 3 | 4 | 7 |
| **totaal** | **849** | **199** | **42** | **224** |

## r2 t.o.v. r1 (zelfde plek op 64×64)
87 px anders, waarvan 6 silhouet (de krulbultjes):
- kop + gezicht 32
- verre achterpoot 34 (kleur)
- hals + lijf 15 (hals lichter + rugkrul + bil)
- staart 6 (pluimbultjes)
- kraag, manchetten, poten, oren: 0

## Afmetingen
Wezen 33 × 48 px, op x 16–48, y 14–61. 15 kleuren + transparant.

## Zwakke punten die nog over zijn
- Het oog is 2 kolommen breed (zoals het model op deze schaal). Op 12× leest het als een staand ovaal of een gleuf, op 1×/2× als een rond kraaloog. Breder dan 2 = groter dan het model.
- De kop blijft van buiten hoekig (rechte rechterrand, platte kruin): dat is het modelsilhouet op 2,3×. De ronding komt nu alleen uit sikkel, kuifboogjes en hooglicht.
- De kuifboogjes zijn op 1× klein. Op 8× lezen ze als twee krullen boven het oog, op 1× vooral als een donkere wenkbrauwlijn.
- De wol op het lijf is nog grotendeels één tint (krullen van het model vallen weg). De rugkrul (19–20,23) is een klein nokje.
- De verre achterpoot gebruikt 6 nergens meer. Zijn omlijning is 1 (zwart), ook aan de lichtkant.
