# Keuring kolibrie pre-evo, kleur r8

Keurder: onafhankelijk (5 nov). Snavel niet gekeurd (Jordi). Vel: `keuring_vel.png` (r8, r8 + voorstel keurder, Taillow, Starly, Fletchling; 5× en 1×, licht en donker).
Coördinaten zijn (x,y). Indexen: 1 zwart, 2 donkerlila, 3 lila schaduw, 6 buik, 9/D/C oranje, F poot donkerst (nieuw in r8: (112,62,28)).

**Controle van de diff r7 → r8:** 56 px gewijzigd, waarvan 26 in alpha, alle binnen de zones van NOTITIES.md. Palet: alleen F is veranderd. Op de rand staan geen lichte kleuren. 619 px.

## 1. Jordi's punten
| Punt | Bevinding | Oordeel |
|---|---|---|
| Pootjes | Groter dan nodig: 11 px breed (x25–35), 4 rijen hoog (43–46), 16 oranje px plus tenen met zwarte punten. Ze vallen meer op dan bij Taillow. Jordi wil "echt kleine pootjes". Daarnaast staan ze naast elkaar op één lijn (beide onderkanten op rij 45/46), zonder perspectief: "ze kunnen niet zomaar naast elkaar". | FAIL |
| Linker buik | De kin-knik is weg, maar er is een nieuwe hoek: de rand loopt 2-2-2 schuin (x16/17/18, rij 22–27) en gaat dan abrupt over in 7 px recht verticaal (x19, rij 28–34). Zo'n concave knik op (19,28) is precies "een gekke hoek"; ook 7 px recht waar het dier rond is, mag niet. De maker noemt het zelf als zwak punt. | FAIL |
| Vleugelschaduw | De grens 8/A loopt per rij op x39,39,39,38,38,37,37,36,35 (rij 28–36): een ronde, versnellende boog. 8 is één rond vlak, A een sikkel die onderaan breed wordt. Leest niet meer als lijn. | PASS |

## 2. Is de belijning van r7 ergens slechter geworden?
- Rug (31,22)→(41,29): runs 1,2,2,2,1,1,1 en v4. Gladder dan r7, overal zwart. PASS.
- Kop linksboven: 4-2-2-1, alleen 2. PASS. Vleugelpunt: rond, zwarte rand. PASS.
- Tapse vleugelrand (2/3/2), staart, onderkant: ongewijzigd ten opzichte van r7. PASS.
- Op de buik na niets slechter geworden.

## 3. Nieuwe problemen
- Alleen de buikhoek en de pootjes hierboven.

## 4. Reparatie (getest in het vel: 42 px ten opzichte van r8, 614 px totaal)
**Buik links: één bolle boog.** Kolomruns 4,3,3,3,2,2,1,1,1,1: x16 rij 22–25, x17 rij 26–28, x18 rij 29–31, x19 rij 32–34, x20 rij 35–36, x21 rij 37–38, daarna zoals r8. Het lijf wordt hooguit 1–2 px voller in de borst.
- (16,24)→2, (17,24)→6 · (16,25)→2, (17,25)→6
- (17,26)→2, (18,26)→6 · (17,27)→2, (18,27)→6
- (17,28)→2, (18,28)→6, (19,28)→6
- (18,29)→2, (19,29)→6 · (18,30)→2, (19,30)→6 · (18,31)→2, (19,31)→6
- (21,38)→2, (22,38)→6

**Pootjes: echt klein, in perspectief.** De nabije poot (x26–28) komt 2 rijen onder het verenpak uit, met twee teentjes C/D en 9 ertussen, en daaronder zwart. De verre poot is 2 px (31–32,43) in 9/F: hij komt maar 1 rij uit, staat dus 1 px hoger, naar rechts/achter en donkerder. In totaal 7 oranje px (r8: 16).
- Verre poot: (31,43)→9, (32,43)→F, (33,43)→1; (31,44)→1, (32,44)→1, (33,44)→0, (34,44)→0, (35,44)→0
- Nabije poot: (29,44)→1, (30,44)→0; (25,45)→0, (26,45)→1, (27,45)→1, (28,45)→1, (29,45)→0, (30,45)→0
- Leeg maken: (31,45), (32,45), (33,45), (34,45), (26,46), (28,46), (31,46), (33,46) → 0
- Ongewijzigd: (27,43)D, (28,43)9, (26,44)C, (27,44)9, (28,44)D, (25,44)1, (26,43)1, (29–30,43)1.

Resultaat onderkant (x20–35):
```
42 .....1333333333311
43 ......1D9119F111..
44 .....1C9D1.11.....
45 ......111.........
```
Optioneel (geen FAIL): (40,29) en (40,30) A→8, dan begint de vleugelsikkel pas op rij 31 als wig.

## Eindoordeel: **TERUG**
2 FAILs: de linker buikrand (concave hoek en 7 px recht) en de pootjes (te groot, geen perspectief). De vleugelschaduw is opgelost en de belijning is verder nergens slechter. Met de 42 px hierboven (getest; geen open randen) is het klaar voor Jordi.
