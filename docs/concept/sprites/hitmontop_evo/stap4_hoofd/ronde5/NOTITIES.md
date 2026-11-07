# Stap 4, hoofd ronde 5 (6 nov): alleen het hoofd, los

Jordi zei letterlijk:
- "het haar is niet anders dan het hoofd, het is hetzelfde materiaal en dezelfde kleur, er zit dus geen streep tussen"
- "kijk aub een keer goed naar hitmontop en stop met dingen verzinnen"
- "rare kippenpoot heeft die ook in zijn haar"
- "de enige streep is wat nu boven zijn ogen zit, maar gezien die haren nu dus naar achter gaan, komt die streep veel hoger te staan, een beetje als een fade"
- "design eerst maar puur het hoofd zonder de rest"

Bestanden: `hoofd_1.png` en `hoofd_2.png` (64×64, alleen het hoofd, op de schermplek waar het later op de vorm komt), `vel_hoofd.png` (per optie op 8×, 2× en 1× op egaal groen, plus Hitmontops spritekop op 8×/2×/1× en de anime), `stap4_r5.py` (met de rasters). Het hoofd is nog niet op de vorm geplakt.

## Wat er is
- **Eén glad geheel.** Schedel, kleine punt en knot vormen samen één omtrek van 1 px E. Binnenin staan geen lijnen tussen haar en kop. Tinten: J als basis, K als schaduwsikkel rechts, P als één klein lichtvlak linksboven (bij optie 1 op de knot, bij optie 2 op de kruin).
- **De enige streep** is Hitmontops flaprand. Die is naar achteren gekamd en staat daardoor hoog op het voorhoofd. Hij loopt in een flauwe V met de punt boven tussen de ogen en heeft de vorm van een fade: het midden is L, (10–15,30–32), en de uiteinden lopen uit in K, (7–9,33) en (16–17,28–29). Hij raakt de omtrek niet. Er zijn geen plooien in de flappen of de knot en niets vertakt.
- **Ogen:** Hitmontops ronde oog (4×4, wit puntje). Links op (11–14, 39–42), rechts op (19–22, 35–38).
- **Mond:** één streepje van 5 px onder de ogen, onderaan het gezicht, met de uiteinden iets omhoog: (17,43), (18,44), (19,44), (20,43), (21,42).
- **Draaiing:** 27° tegen de klok in. De ogen staan schuin en de kruin wijst naar linksboven.
- **Maat:** 419 px (optie 1) en 415 px (optie 2), tegen 375 px in ronde 4 (ronde 3b was 489 px, inclusief zware rand). Het hoofd valt binnen x1–25 en y21–47. Het raakt geen pixel van het lijf van `stap3b/optie_C` en heeft geen open randen (met een script gecontroleerd).

| optie | knot | punt |
|---|---|---|
| 1 | op de kruin; de kop loopt door in de knot, met een inkeping rechts bij (11,27) | steekt linksboven uit de knot, tip (5,21) |
| 2 | achterop links, x1–6 en y26–31, vast aan de kop | op de kruin, uit de kop zelf, tip (8,23) |

## Eerlijke zwakke punten
- **Optie 1: de knot leest nauwelijks als knot.** Knot en punt vormen samen een druppel- of uienpunt. Op 1× lijkt het meer op Hitmontops spitse kop dan op opgeknot haar.
- **Optie 2: de knot kan als oortje lezen.** Hij is een losse bol links. De punt is klein: 1–2 px breed op de kruin.
- **De fadestreep kan als litteken of wenkbrauw lezen.** Hij staat midden op het voorhoofd. Op 1× is hij nauwelijks zichtbaar.
- **Het gezicht is kaal en lief.** Zonder de fronslijn boven de ogen ontbreekt Hitmontops strenge blik. Het leest chibi-achtig.
- **Mond en lijnen.** De mond zit rechtsonder door de draaiing en is klein. De schaduwsikkel rechts is K naast de omtrek, met een harde rand.

## Pixeldump-check (uit de PNG's)
### Optie 1 (uit hoofd_1.png; kleuren: 1 E J K L P)
```
x: 01234567890123456789012345
21 .....E....................
22 ....EPE...................
23 ....EPJE..................
24 ....EJJEEEE...............
25 ....EPPJJJKE..............
26 ....EPJJJJKE..............
27 ....EJJJJJKEEEEEEE........
28 ...EJJJJJJJJJJJJJKEEE.....
29 ....EJJJJJJJJJJJKJJJJE....
30 ....EEJJJJJJJJJLJJJJJJE...
31 ......EJJJJJJJLJJJJJJJKE..
32 .....EJJJJLLLLJJJJJJJJKE..
33 .....EJKKKJJJJJJJJJJJJJKE.
34 ....EJJJJJJJJJJJJJJJJJJKE.
35 ....EJJJJJJJJJJJJJJJEEJKE.
36 ....EJJJJJJJJJJJJJJE1EEJKE
37 ....EJJJJJJJJJJJJJJEEEEJKE
38 ....EJJJJJJJJJJJJJJJEEJKE.
39 ....EJJJJJJJEEJJJJJJJJJKE.
40 ....EJJJJJJE1EEJJJJJJJJKE.
41 ....EJJJJJJEEEEJJJJJJJKE..
42 .....EJJJJJJEEJJJJJJJEJE..
43 .....EJJJJJJJJJJJEJJEJJE..
44 ......EJJJJJJJJJJJEEJJE...
45 .......EJJJJJJJJJJJJJE....
46 ........EEJJJJJJJJJJE.....
47 ..........EEEEEEEEEE......
```
### Optie 2 (uit hoofd_2.png; kleuren: 1 E J K L P)
```
x: 01234567890123456789012345
21 ..........................
22 ..........................
23 ........E.................
24 ........EE................
25 ........EPE...............
26 ..EEEE..EJE...............
27 .EJJJJE.EJKEEEEEEE........
28 .EJJJJE.EJJJJJJJJKEEE.....
29 .EJJJKJEJJPPJJJJKJJJJE....
30 .EJJKKJJJJPJJJJLJJJJJJE...
31 ..EEJJJJJJJJJJLJJJJJJJKE..
32 ....EJJJJJLLLLJJJJJJJJKE..
33 .....EJKKKJJJJJJJJJJJJJKE.
34 ....EJJJJJJJJJJJJJJJJJJKE.
35 ....EJJJJJJJJJJJJJJJEEJKE.
36 ....EJJJJJJJJJJJJJJE1EEJKE
37 ....EJJJJJJJJJJJJJJEEEEJKE
38 ....EJJJJJJJJJJJJJJJEEJKE.
39 ....EJJJJJJJEEJJJJJJJJJKE.
40 ....EJJJJJJE1EEJJJJJJJJKE.
41 ....EJJJJJJEEEEJJJJJJJKE..
42 .....EJJJJJJEEJJJJJJJEJE..
43 .....EJJJJJJJJJJJEJJEJJE..
44 ......EJJJJJJJJJJJEEJJE...
45 .......EJJJJJJJJJJJJJE....
46 ........EEJJJJJJJJJJE.....
47 ..........EEEEEEEEEE......
```
