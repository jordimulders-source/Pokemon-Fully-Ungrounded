# Stap 4, hoofd ronde 3b (pixelreparaties, 6 nov)

Basis: `ronde3/optie_1M-r3-knot.png`; r3 vervalt. Alleen de punten uit `ronde3/vel_hoofd.png.keuring.md` zijn veranderd. Bestanden: `optie.png`, `hoofd.png`, `vel_hoofd.png`, `controle.txt`, `stap4_r3b.py` (met het raster).

Letters in de dumps (zelfde als de keuring): J = basishuid (222,189,131), K = middentint (180,139,90), L = donkerbruin (131,90,41), P = glim (255,222,156), E = omlijning, `.` = leeg, `?` = pixel van de vrije voet (bevroren, geen hoofd). De dumps zijn gemaakt uit `optie.png` zelf.

## 1. Knot in haartinten (+ polijsten: 1 px van de vakrand)
Basis K, schaduwsikkel L rechtsonder, J alleen als glim van 3 px linksboven: (3,21), (2,22), (3,22). De knot begint nu op x1, dus x0 is leeg. Hij raakt de voet (7–9,20) niet: (6,20) is leeg. De kamstreep (11,26) loopt door de hals in: (9–10,26) zijn L in plaats van omlijning.
```
x: 012345678 9 10       (y20–27, x0–10)
20 ...EEE.?EE.
21 ..EJKKE....
22 .EJJKKKE...
23 .EKKKKLLE..
24 .EKKLLEEEE.
25 ..EKLLELKKE
26 ...EEELKKLL
27 ......EELKL
```

## 2. Voorhoofdslijn weg, haargrens schuin (links lager)
(14–21,30) is van L naar K gegaan. (19–23,30) is huid J. Op x10–13 loopt het haar K door tot y31. De grens ligt dus op y29 rechts, y30 in het midden en y31 links, en loopt via de bestaande boog naar de knot.
```
x: 10.............25   (y29–31)
29 KKKKLKKKKKKLKKEE
30 KKKKKKKKKJJJJJKK
31 KKKKJJJJJJJJJJKK
```
Polijsten: de reep x7–8, y30–33 is haar K tot de omtrek. De L op (8,30) en (8,33) is de kamstreep naar de knot.
```
x: 78
30 KL
31 KK
32 KK
33 KL
```

## 3. Mond los van de schaduw
(21–23,44) en (24,42) zijn J. Polijsten: (18,42) is van L naar K gegaan; (17,42) blijft J tussen de plooi en de mond. Onder de mondbodem (20–22,43) is y44 helemaal huid.
```
x: 16.......25   (y42–44)
42 EJKEJJJEJJ
43 JJJJEEEJJK
44 JJJJJJJJEE
```

## Bevroren
`controle.txt`: de pixeldiff t.o.v. `stap3b/optie_C.png` is 0 buiten de zone. De zone bestaat uit het nieuwe hoofd (489 px) plus het oude hoofd (169 px), samen binnen x1–29, y20–47. Ogen, hoorn, omtrek, fronslijnen en mondvorm zijn ongewijzigd t.o.v. r3-knot. Geen open randen.

## Zwakke punten
- (6,21) van de knot raakt de voet (7,20) schuin, met een hoekje.
- De haarkap rechts (x24–26, y30–34) en de wangschaduw zijn beide K en lopen in elkaar over (de keurder vond dat acceptabel).
