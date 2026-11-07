# Stap 4, hoofd ronde 4 (6 nov)

Opdracht: Jordi's woorden over ronde 3b plus zijn krabbel (`referenties/krabbel_hoofd_jordi.png`), en de aanvulling "het hoofd onderste boven is wel erg gek". Het hoofdpunt is dat het hoofd onmiskenbaar rechtop leest: de kruin met de kleine punt en het opgeknotte haar boven, de V van de haarlijn boven de ogen, de ogen in het midden en de mond onderaan. Alles is tegen de klok in gedraaid.

Bestanden: `optie_A/B/C.png` (hoofd op de vorm), `hoofd_A/B/C.png` (hoofd los op 8×, naast Hitmontops front en de anime), `vel_hoofd.png` (per optie 8× uitsnede, 1× en 2× naast Hitmontop), `controle.txt`, `stap4_r4.py` (de rasters staan erin als tekst).

## Werkwijze
- De omtrek is eerst als gids gedraaid: kop, haarmassa boven de V, knot en hoorn, alles in één kopkader. Ronde 3b stond al ongeveer 12° gedraaid. A en C staan op 27°, B op 42°.
- Daarna is alles met de hand per pixel gezet: de V, de haarstrepen, de knot, de hoorn, de ogen, de mond en de tinten.
- Kleuren: alleen Hitmontops normal.pal. Huid, haar, knot en hoorn zijn één kleurgroep: P (glim), J (basis), K (midden) en L (lijn), met E als omlijning. Het haar onderscheidt zich alleen door lijnen: de V in E en de kamstrepen in L met een K-groef. Er is geen aparte haarkleur.
- Ogen: Hitmontops ronde oog uit anim_front.png, 4×4 met één wit puntje linksboven (`.EE. / E1EE / EEEE / .EE.`). Beide ogen zijn hetzelfde type.
- Mond: één streepje van 5 px. De uiteinden staan iets omhoog en de lijn volgt de draaiing. Er staan geen schaduwen omheen.
- De kin heeft geen donkere band. De schaduw is alleen een K-sikkel langs de rechterrand, y33–41, en stopt boven de mond.

## Opties
| optie | draaiing | knot | punt (hoorn) |
|---|---|---|---|
| A | 27° | op de kruin, om de punt heen | steekt linksboven uit de knot (tip (7,22)) |
| B | 42° | op de kruin, om de punt heen (verschoven naar linksboven) | steekt links uit de knot (tip (4,24)) |
| C | 27° | achterop (links, zoals ronde 3b) | op de kruin, door het haar heen (tip (9,24)), met een L-band van het haar over de voet |

A en B volgen Jordi's woorden letterlijk: "opgeknot, om een kleinere punt heen". C volgt de krabbel zoals die getekend is: de punt bovenop, en de bestaande knot links is niet doorgestreept. **Vraag aan Jordi: hoort de knot óm de punt (A/B), of zit de punt los in het haar met de knot achterop (C)?**

## Pixeldump-check van de claims (gemaakt uit de PNG's zelf)
Letters: P (255,222,156), J (222,189,131), K (180,139,90), L (131,90,41), E (16,16,16), 1 = wit, `.` = leeg.
- **Mond onder de ogen, onderaan het gezicht.** Bij A/C zitten de ogen op y36–42 en de mond op (16,43) (17,44) (18,44) (19,43) (20,42). Daaronder ligt alleen nog J (y44–45) en dan de omtrek op y46. Bij B zitten de ogen op y33–42 en de mond op (17,42) (18,43) (19,43) (20,42) (21,41).
- **Ogen zijn rondjes met één wit puntje.** A/C: links (12–15, 39–42) met wit op (13,40), rechts (19–22, 36–39) met wit op (20,37). B: links (13–16, 39–42), rechts (19–22, 33–36).
- **De V-haarlijn zit direct boven de ogen.** A/C: de linkerarm loopt over (7–11,37) en (12–16,36), met 2 px huid boven het linkeroog. De rechterarm loopt steil van (17,35) via (18,34) en (19,33) tot (22,30). Hij heeft 1 px huid diagonaal naar het rechteroog en vormt zo de frons.
- **Haar, knot en hoorn zijn één kleurgroep.** In de hoofdzone komen alleen de 6 kleuren P, J, K, L, E en wit voor (gecontroleerd per optie).
- **Pixeldiff 0 buiten de hoofdzone** ten opzichte van `stap3b/optie_C.png` (zie `controle.txt`). Het nieuwe hoofd raakt geen enkele pixel van het lijf. Er zijn geen open randen (gecontroleerd met een script). De knot van C begint op x1, dus x0 blijft leeg.

### Optie A (uit optie_A.png, x0–24, y22–46)
```
x: 0123456789012345678901234
22 .......E.................
23 ......EPE................
24 ......EPJE...............
25 ......EJKEEEE............
26 .....EJEEJKKKEEEEEE......
27 .....EJJKKLKKEJJJJJEE....
28 .....EJKKKKLEJJJLKJJJEE..
29 .....EKKKKLKEJJJJLLKJJJE.
30 ......EEKKEEJLKJJJJLKJEE.
31 ......EJEEJLKJLKJJJJLEJE.
32 .....EJLKJJLKJLKJJJJEJJE.
33 .....EJLKJJLKJJLKJJEJJJKE
34 .....EJLKJJJLKJJLKEJJJJKE
35 ....EJJJLKJJLKJJJEJJJJJKE
36 ....EJJJLKJJEEEEEJJJEEJKE
37 ....EJJEEEEEJJJJJJJE1EEKE
38 ....EEEJJJJJJJJJJJJEEEEKE
39 ......EJJJJJJEEJJJJJEEJKE
40 ......EJPPJJE1EEJJJJJJKE.
41 ......EJPJJJEEEEJJJJJJKE.
42 .......EJJJJJEEJJJJJEJE..
43 ........EJJJJJJJEJJEJJE..
44 .........EEJJJJJJEEJJE...
45 ...........EEEJJJJJEE....
46 ..............EEEEE......
```
### Optie B (uit optie_B.png, x0–24, y22–46)
```
x: 0123456789012345678901234
22 .........................
23 .........................
24 ....E....................
25 ...EPE...................
26 ...EPJEEEEE.EEEEEEE......
27 ....EEEJJKKEJJJLLKJEE....
28 .....EJJKKLKEJJJJLLKE....
29 .....EJKKKKLEJJJJJJLEE...
30 .....EKKKKKLEJJJJJJEJJE..
31 .....EKKKKLLELKJJJJEJJJE.
32 .....EEKKLLEJJLKJJEJJJJE.
33 .....EJEEEEJJJJLKEJJEEJKE
34 ....EEJJJJLKJJJJLEJE1EEKE
35 ....EJLKJJJLKJJJEJJEEEEKE
36 ....EJJLKJJLKJEEJJJJEEJKE
37 ....EJJLKJJJLEJJJJJJJJJKE
38 ....EJJJLKEEJJJJJJJJJJJKE
39 ....EJJJEEJJJJEEJJJJJJJKE
40 .....EEEJJJJJE1EEJJJJJKE.
41 ......EJPPJJJEEEEJJJJEJE.
42 .......EPJJJJJEEJEJJEJJE.
43 ........EJJJJJJJJJEEJJE..
44 .........EJJJJJJJJJJJE...
45 ..........EEEJJJJEEEE....
46 .............EEEE........
```
### Optie C (uit optie_C.png, x0–24, y22–46)
```
x: 0123456789012345678901234
22 .........................
23 .........................
24 .........E...............
25 ........EPE..............
26 ........EPJEEEEEEEE......
27 ..EEEE.EJJKEJJJJJJJEE....
28 .EJJKKEKLLLKEJJLJJJJJEE..
29 .EJKKKEJJJJJLJJKLLJJJJJE.
30 .EKKKLEJJJJJKLJJKKLLJJEE.
31 .EKKLEJJJLJJJKLJJJKKLEJE.
32 ..ELLEJJJKLJJJKLJJJJEJJE.
33 ...EEEJLJJKLJJJKLJJEJJJKE
34 .....EJKLJJKLJJJKLEJJJJKE
35 ....EJJJLJJJKLJJJEJJJJJKE
36 ....EJJJKLJJEEEEEJJJEEJKE
37 ....EJJEEEEEJJJJJJJE1EEKE
38 ....EEEJJJJJJJJJJJJEEEEKE
39 ......EJJJJJJEEJJJJJEEJKE
40 ......EJPPJJE1EEJJJJJJKE.
41 ......EJPJJJEEEEJJJJJJKE.
42 .......EJJJJJEEJJJJJEJE..
43 ........EJJJJJJJEJJEJJE..
44 .........EEJJJJJJEEJJE...
45 ...........EEEJJJJJEE....
46 ..............EEEEE......
```

## Eerlijke zwakke punten
- **Het gezicht is leeg en lief.** De onderste helft is een groot J-vlak met een kleine mond. Op 1× leest het als een vriendelijk koppie ("dumpling"), minder als vechter. De mond is 5 px en schuin. Op 1× kan hij als grijnsje of smirk lezen, en niet als een rechte, blije streep.
- **Haarstrepen.** Er zijn 4 L-lijnen, elk met een K-groef. Op 8× is dat druk ("arcering") en het neigt naar de kamstreep-ruis die we niet willen. Op 1× is het prima. Met 3 lijnen wordt het rustiger.
- **Hoek linksonder te zwart.** Waar de overhang van het haar de V raakt, zijn 3 px E naast elkaar: A/C (4–6,38), B (5–7,40).
- **Hoorn klein.** In A leest hij als een puntje op de knot. In B is hij op 1× bijna een spikkel. C heeft de duidelijkste punt.
- **Haar als kap?** Links steekt het haar 1 px uit over het gezicht (een trapje in de omtrek, zoals Hitmontops rand). Dat helpt het als haar te lezen. Het kan wel als helm of "eikeldop" ogen, zeker in A.
- **Maat.** Het hoofd is 368–386 px tegen 489 px bij ronde 3b (inclusief knot). Het gezicht is ongeveer even groot, x5–24 en y26–46. Het is dus niet groter geworden.
- **42° (B).** Daar valt de linkerarm van de V naar links omlaag tot y40. Dat klopt met de draaiing, maar het gezicht oogt erdoor scheef.
