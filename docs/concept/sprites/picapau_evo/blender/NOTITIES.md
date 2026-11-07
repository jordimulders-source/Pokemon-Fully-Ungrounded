# Evo van Picapau: 3D-model (stap 2), notities van de maker

Model: `picapau_evo.py` (eigen bestand; `../../picapau/blender/picapau.py` niet aangeraakt). Zelfde opbouw als Picapau: één huid als smooth union van afstandsvelden (marching cubes), kleurvlakken per vlak, snavel/oog/tong/pootjes los; Workbench, ortho 64 BU = 64×64, 512 px = 8×.
Draaien: `python3.11 rondom.py` (rondom-vel `rond_v1/vel.png`), `python3.11 standen.py` (A/B/C + tong-variant + `standen/standen.png`). Pillow voor python3.11: `python3.11 -m pip install --ignore-installed pillow` (de systeem-PIL werkt niet met 3.11).

## Wat ik bouwde
- **Nieuw t.o.v. Picapau:** de kop (kop, kuif, achterkuif, snavel, oog, wang) heeft een **eigen draai om de nek** (`kop_draai`, bovenop de lijfdraai) en de hele romp kan **voorover** kantelen rond de heup (`voorover`), terwijl de pootjes blijven staan. Daarmee: kop meer naar de kijker dan het lijf, geen profielkop.
- **Lijf:** groot opgeblazen ei (14 × 13,5 × 13,5) + opgezette borst + dikke nek; grote crème buikovaal (Raichu-buik). Dijen in de huid, korte stevige pootjes (2 voor, 2 achter, als platte tenen).
- **Vleugels half open, dreigend opgetrokken:** arm schuin omhoog/naar buiten, brede handplaat met vijf ronde handpennen in een waaier, armpennen naar achter-onder. De verre vleugel steekt boven de rug uit achter de kop. Ronde lichte stippen alleen op de dekveren (familie Picapau, geen schubben).
- **Kuif:** twee brede, platte kuifpunten die omhoog gaan en aan de top als een haak naar buiten en weer omlaag krullen (Raichu-oren), crème, geen zwarte toppen. Kort rafelig achterkuifje zoals Picapau.
- **Staart:** lange pluim uit de stuit, eerst naar rechts-boven, dan omlaag en onder het lijf door naar voren (achter de nabije poot langs), eindigend in een **platte gele bliksemschicht** (2 zigzags) linksonder die naar voren-boven wijst. Bliksem ≥ 4 BU breed (op 1× 3–4 px), de punt zelf loopt taps toe.
- **Kop:** grote ronde kop (9,6), groot donker oog met glans (alleen het nabije oog: het verre oog stak als bultje uit de omtrek), rode wangvlek, lange beitelsnavel (15 BU, iets omhoog).
- Kleuren zijn alleen een gids (Workbench maakt alles bruiner en grijzer dan het materiaal): lijf oranje-kastanje, vleugels donkerder kastanje, staart roodbruin, kuif en buik crème, bliksem geel.

## Standen (`standen/`, elk `_8x.png` + `_1x.png`; vel `standen.png` met Picapau (af) en Raichu Gen 1, 1× en 4×)
| stand | lijf | kop erbij (totaal) | voorover | kantel | 1× px |
|---|---|---|---|---|---|
| A | 30 | 20 (50) | 15 | 8 | 2111 |
| B | 20 | 25 (45) | 22 | 12 | 1910 |
| C | 40 | 20 (60) | 10 | 8 | 2020 |
Picapau (af) heeft ±830 px: de evo vult het frame 2,3–2,5× zo veel. Elke stand is automatisch passend gezet (1 px marge).
Tong-variant: `standen/C_tong_8x.png` / `C_tong_1x.png` (snavel iets open, lange roze tong hangt in een boog naar beneden).

## Mijn keuze: C
- Beide kuifkrullen lezen op 1× als haken (in A en B valt de nabije kuifkrul over de verre vleugel en wordt een crème vlek).
- Kop het duidelijkst 3/4 met het oog vrij in het kopvlak; bliksempunt vrij linksonder.
- Nadeel van C t.o.v. A: de snavel is iets meer verkort (kop totaal 60°). A is het compromis als de snavel belangrijker is; B is het meest dynamisch (uitval naar voren) maar daar overlappen kuif en vleugel het meest.

## Controle op 1× (64 px)
- **Snavel:** leest, maar kort: ±5 px in C, ±6 px in A (verkorting door de kopdraai). De onderkant van de kegel is donker in de render, waardoor hij op 1× soms op een open snavel lijkt.
- **Kuifkrullen:** C: beide haken leesbaar (2–3 px dik, gat ±2 px). A/B: alleen de verre haak; de nabije smelt samen met de verre vleugel.
- **Staart:** leest als brede bruine boog onder het lijf; 3–5 px dik.
- **Bliksempunt:** leest in alle drie als gele zigzag, 3–4 px dik; alleen de uiterste punt is 1–2 px.
- **Tong-variant:** de tong is op 1× 2 px dik en leest als een roze sliert onder de snavel.

## Zwakke punten (eerlijk)
1. **Kuif lijkt op hoorns** (ram/geit, of een duiveltje), vooral in C en van voren. Dat zijn de "krullende oren" die gevraagd zijn, maar ze lezen niet als veren. Mogelijke variant: kuifpunten met een rafelige rand of een veerinkeping.
2. **Vleugel is druk:** veel punten en veel stippen; op 1× wordt de vleugel een bruin stekelig vlak met een raster van stipjes (in A/B lijkt het van ver op een egel). Minder stippen of een dichtere vleugelrand zou rustiger zijn. Van voren (rondom 90°) zijn de vleugels smal: ze staan opgetrokken langs het lijf, niet breed gespreid.
3. **Staart is een gladde worst**, geen veerpluim, en de boog is meer een J/U onder het lijf dan een echte S. De S zit alleen in de bliksem aan het eind.
4. **Snavel kort en kegelvormig** door de kopdraai (zie boven).
5. **Raichu-gelijkenis:** de bliksemstaart linksonder + oorkrullen + crème buikovaal zijn duidelijk Raichu Gen 1, maar het blijft een dikke vogel met vleugels; ik vind het minder Raichu dan Picapau Pikachu is (zoals gevraagd). Wel een algemene vogel-lijfvorm die naar Fletchinder/Pidgeotto kan neigen; de kuif en de bliksem maken hem eigen.
6. **Pose:** anders dan onze vogels door de opgetrokken vleugels, de voorover-uitval en de krullende staart, maar het lijf staat nog vrij rechtop (geen echte legendary-boog zoals Articuno). Geen tweede, meer gekrulde pose gemaakt.
7. **Tong-variant:** lijkt meer op een worm in de snavel dan op een spechtentong; de snavel staat nauwelijks zichtbaar open. Jordi's verwachting ("ik denk dat het niet lukt") klopt grotendeels.
8. Kleuren in de render zijn te bruin/grijs (Workbench); alleen vorm beoordelen. Rondom: van de andere kant (180°) is er geen oog (alleen het nabije oog is gebouwd).
