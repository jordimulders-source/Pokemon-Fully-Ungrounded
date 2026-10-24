# Olinguito finale: werklog (24 okt)

Basis: `ronde23/anim_front.png`. Jordi: "ronde 23 zit goed", maar de kop is te groot en de 4e poot ontbreekt; formaat naar fase 1. Alles met de hand in tekstrasters (`bron/`); bouwen: `python3 bron/maak.py && python3 bron/bouw.py`.

## Iteraties
| # | Wat ik probeerde | Wat faalde bij de eigen keuring | Wat ik deed |
|---|---|---|---|
| 1 | Achterhoofd 1-3 px naar binnen, achterlijf in één keer opnieuw (patch met losse rijen) | Rommelige rijen (tellen ging mis, losse pixels), J-krul raakte de dij (lus dicht), verre achterpoot een donkere klodder | Weggegooid. Werkwijze vervangen door rijen met absolute x (`teken.py`) en de J-staart als bevroren blok (`staart.py`) |
| 2 | J-staart exact (pixel voor pixel) 2 px naar rechts en 3 omhoog; romp/rug, dij, nabije achterpoot en verre achterpoot opnieuw | Verre achterpoot tussen de poten (OORDEEL-voorstel) zou samen met de verre voorpoot vooruit staan: **telgang** (AFGEKEURD 21b) | Verre achterpoot **rechts achter** de nabije, onder de staartkrul (diagonale gang zoals Galar-Linoone); staartwortel stijgt boven de rug (tegenwicht A3) |
| 3 | Nabije achterpoot zonder hak | C4: rechte kolom, stokpoot | Knie voor, hak naar achteren (x46), middenvoet weer naar voren |
| 4 | Klauwen ronde 23 bekeken op 8x | Grijs-witte klodders (Chernobyl-punt "klauwen als klodders") | Twee haken per voorpoot: brede wortel tegen de poot, kromming, punt omlaag (Sandslash). Eerste versie te dun/lang (hark) → dikker en korter; open randen aan de onderkant gedicht met dubbele `11` |
| 5 | Formaat: 1064 px na de nieuwe achterkant | D1 (fase 1 ≤ 950) | Stroken weggeknipt zonder kenmerken (§15): één poten-/dijrij en één rij onder de kaak (poten korter en stomper, D3). Eerste schedelknip pakte de oorbasis van het verre oor: teruggedraaid, de kenmerkloze rij eronder geknipt. Buikboog (lucht, A4), dij-achterkant kleiner (lucht naar de staart), teenscheiding |
| 6 | Kopaandeel nagemeten met het echte kopvak | 41,9 % (ronde 23: 44 %): nog boven de snuitdieren (25–41 %, mediaan 34 %), dus Jordi's "kop te groot" niet echt opgelost | Nabije oor als geheel 2 px naar links (knippen/plakken, diff 0); schedel achter het masker 2 kolommen korter (kenmerkloze vacht); nek en rug 2 px naar links mee. Kop 39,3 %, totaal 936 px |
| 7 | Achterhoofd na stap 6 | Achterkant van de kop werd een verticale rechte rand; kop/nek-lijn een rechte zwarte streep van 6 | Achterhoofd weer als boogje (32-33-33-34-34-33-33); kop/nek-lijn met wangbolling |
| 8 | Nabije voorpoot | Onderrand onderarm 7 px recht (plank) | Onderarm loopt in een boog op naar de elleboog |
| 9 | Frame 2 met een naad per kolom | J-krul brak op de naad (open rand, losse punt) | Frame 2 uit dezelfde tekening: één strook minder weggeknipt → kop, romp en staartwortel 1 px hoger, poten en hangende staart 1 rij langer, voeten blijven staan |

## Eindstand
- 936 px (frame 1), box 50×33, soliditeit 0,71, symmetrie 0,50, kop 39 % van het oppervlak en 58 % van de hoogte.
- Gezicht (neus, snuit, masker, oog, boogje, grijns, verre oor): pixeldiff 0 met ronde 23; nabije oor: diff 0 (2 px verschoven); palet ongewijzigd.
- J-staart: dezelfde pixels; de hangende rechte strook is 2 rijen korter (frame 2: 1) doordat de stroken door het hele lijf zijn geknipt.
- Volledige keuring: `KEURING.md`.

## Lessen (voor Claude om over te zetten)
- Een "verre poot tussen de nabije in" (checklist C2/Mightyena) geeft telgang als de verre voorpoot al vooruit staat: controleer de diagonaal vóór je het skelet volgt.
- Kopaandeel altijd meten met het echte kopvak (neuspunt t/m achterhoofd, oortop t/m kin); een knip in de poten verlaagt het totaal en verhoogt dus het kopaandeel.
- Stroken knippen door het hele lijf raakt ook de staart en de oren: controleer per knip welke bevroren pixels in die rij zitten (eerste schedelknip pakte de basis van het verre oor).
- Klauwhaken diagonaal: waar de haak smaller wordt én opschuift, eindigt de rij op `11`, anders ontstaan open randen aan de onderkant.
- Frame 2 als "dezelfde tekening met één strook minder weggeknipt" is veel veiliger dan een naad per kolom.
