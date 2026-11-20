# Keuring Coathief r3: schaduw, kleur en belijning (Dragonfly Cave / Gen 3)

Gekeurd: `coathief_r3.png` (`r3.txt` + `palet.txt`), 8× naast Mightyena, Poochyena, Linoone, Zigzagoon en Furret (eerste frame van `anim_front.png`), op witte en donkere achtergrond. Silhouet, vorm, crème oogaftekening, rood oog, zwarte oren en staartringvolgorde zijn bevroren en niet gekeurd. Elke reparatie hieronder is in een kopie gesimuleerd (geen vormwijziging, alpha identiek).

## Oordeel: BIJNA

Wat al goed is: lijf heeft echte selout (bruin_schaduw 5) aan de lichte bovenkant en zwart aan onder- en rechterkant (rechts 100% zwart, onder 100%; Mightyena 98% / 91%); binnenlijnen in het lijf (schouder, dijbeen) staan in de donkere tint van het vlak (5), niet in zwart; bruine tintstappen 61 → 95 → 130 (stappen 34/35) zitten precies in de Gen 3-band (±30–40); verre middenpoot staat in de schaduwtint (E1); aandeel zeer donkere pixels 0,31 (Mightyena 0,48, Poochyena 0,18): past bij een Dark-type met zwarte kop.

Wat tegenhoudt:
1. **Zwart heeft geen bruikbare schaduwstap.** Helderheid omlijning 16 → zwart_schaduw 37 → zwart_midden 52 → zwart_licht 86: de stap schaduw→midden is maar **15**, dus de kop leest als één vlak plus een hooglicht. Mightyena's zwarte vacht: 8 → 32 → 62 (stap 30). Gevolg: de schaduw die er wel staat (kaak, oor, poten) is onzichtbaar.
2. **Kop heeft geen schaduwsikkel.** Hooglicht (4) op schedel en snuitrug klopt, maar de kant van het licht af (wang → kaak → hals, rechtsonder) heeft hooguit 1 px schaduw en de hele onderkaak x13–23 staat in midden (3) direct op de zwarte lijn. DFC §5: schaduw volgt de "evenaar" als sikkel aan de kant van het licht af.
3. **Kop volledig zwart omlijnd, ook aan de lichtkant.** Boven/links van de kop staat 100% omlijning (16) tegen het hooglicht (86): harde tekenfilmrand. Mightyena gebruikt op de lichtkant van zwarte vacht zijn schaduwtint als selout (boven 18× idx 6, links 31× idx 2). DFC §8 / SPRITE_KERN: zwart aan de schaduwkant, selout aan de lichtkant.
4. **Crème heeft geen eigen omlijningstint.** crème_schaduw 8 (L128) is tegelijk de schaduwtint in de ringen én de buitenlijn aan de lichtkant van staart en tenen (20 px op de buitenrand). Te licht als lijn (Linoone: crème-omlijning L109/81) en de stap 8→9 is **67** tegen 9→10 = 42: de crème schaduw springt eruit als bruine vlek. DFC (recolor-regel 4): "create a separate outline highlight color that's darker than the shadow color".
5. **Nabije voorpoot (x26–33, y53–60) mist de lichtrand** die de nabije achterpoot wel heeft (`143321`): hij staat als `1 3 3 2 2 2 1`, half om half, en leest daardoor even donker als de verre poot.

## MOET (per script toe te passen; palet eerst)

### Palet (huidige indexen; 13 → 14 kleuren incl. transparant)
| idx | nu | wordt | waarom |
|---|---|---|---|
| 2 zwart_schaduw | (36,37,38) L37 | **(32,33,36)** L33 | stap tot midden ±25 (Mightyena 32→62); iets koeler (DFC: schaduw licht richting blauw, Mightyena/Poochyena-zwart (56,64,64)/(48,56,56)) |
| 3 zwart_midden | (50,52,53) L52 | **(56,58,62)** L58 | idem; blijft duidelijk zwart (getest: L65 werd leigrijs, te ver) |
| 4 zwart_licht | (84,87,88) L86 | **(88,92,98)** L91 | stap 33 boven midden |
| 8 crème_schaduw | (150,124,92) L128 | **(176,150,112)** L153 | stap tot crème_midden 42, gelijk aan 9→10 |
| 13 (nieuw) crème_omlijning | – | **(120,96,68)** L100 | eigen selout voor crème (Linoone 128,104,88 / Furret-patroon) |

### Belijning crème (8 → 13 op de buitenrand; alleen pixels die aan transparant grenzen)
(48,2) (49,2) (47,3) (46,4) (45,5) (45,6) (52,7) (52,12) (52,13) (52,14) (52,15) (51,20) (51,21) (51,22) (49,27) (48,28) (47,29) (24,59) (23,60) (22,61) → **13**.
Binnenpixels met 8 blijven 8 (schaduw in ringen en tenen).

### Kop: selout aan de lichtkant (1 → 2)
(15,30) (18,30) (19,30) (14,31) (23,31) (14,32) (14,33) (13,34) (13,35) (12,36) (12,37) (12,38) (12,39) (12,40) (12,41) (11,42) (10,43) (9,44) (8,45) (7,46) (20,48) → **2**.
Doorlopend van oortip via schedel en wang tot de neuspunt, zodat er geen zwart/selout om-en-om ontstaat. Onder- en rechterrand van de kop blijven 1. (Bron: Mightyena-zwart, DFC §8 overgang "zwart → zwart met omlijningsbasis → omlijningsbasis".)

### Kop: schaduwsikkel wang → kaak (3 → 2)
Wang (2 px breed bij de hals): (25,36) (25,37) (25,38) (24,39) (24,40)
Onderkaak (1 px langs de onderrand): (23,43) (22,43) (21,44) (20,44) (19,45) (18,45) (17,45) (16,46) (15,46) (14,47) (13,47)
→ **2**. Sluit aan op de bestaande 2 bij (24,41) (23,42) (24,42) en de snuitonderkant (10–12,46–48). Raakt de crème aftekening en het oog niet. (DFC §5 evenaar/sikkel; Poochyena en Mightyena: kaak en hals donker, schedel licht.)

### Nabije voorpoot: lichtrand (3 → 4)
(29,54) (29,55) (28,56) (28,57) (27,58) (26,59) (26,60) → **4**. Geeft hetzelfde profiel als de nabije achterpoot (`1 4 3 3 2 1`); verre middenpoot blijft in 2/3 (E1/C6, Mightyena-poten).

## MAG
- **Bruin hue-shiften** (DFC "Kleuren": schaduw iets naar rood/paars, licht iets naar geel; maakt het "warm roodbruin" i.p.v. oranje): 5 → (92,44,28), 7 → (188,124,62); 6 blijft (142,82,38). Helderheid gelijk. Getest: rustiger, roder in de schaduw.
- **Vachtgrens 7/6 op de rug karten** (DFC §7 vacht: grens gekarteld; nu een regelmatige trap 44-40-36-33-33-30): (41,35) (42,35) (34,37) (35,37) 6 → **7** (plukjes naar achter-onder).
- **(29,33) 7 → 5**: los lichtpuntje (1 px) in de bovenste selout-hoek bij de nek; met 5 loopt de selout (30–31,33)–(32–34,32) door.
- **Crème ringen**: het lichtste crème (10) ligt overal als 2-px band direct tegen de lichte rand (`D A A 9 9 8 1`), parallel aan de omtrek. Kan een tikje naar binnen (Furret-staartstrepen), maar als cilinder is het verdedigbaar; alleen aanpakken als Jordi de staart "streperig" vindt.
- **Klauwen**: nu alleen 9/8 (lezen als één klodder op 1×). Eén pixel 10 per klauwtip, bijv. (17,53) en (26,61), naar Mightyena-klauwen (wit + grijs + zwart).
- Rechter schaduwband van het lijf (x45–49, y35–49) is 2–4 px en vrijwel evenwijdig aan de rand; mag onderin 1 px breder (sikkel), maar is niet storend.

## Metingen
| | rand boven zeer donker | links | onder | rechts | zeer donker totaal |
|---|---|---|---|---|---|
| Coathief r3 | 0,66 | 0,76 | 1,00 | 1,00 | 0,31 |
| Mightyena | 0,85 | 0,71 | 0,91 | 0,98 | 0,48 |
| Poochyena | 0,84 | 0,70 | 0,90 | 0,88 | 0,18 |
| Linoone | 0,28 | 0,57 | 0,87 | 0,77 | 0,14 |

Tintstappen (L): zwart 16/37/52/86 (stappen 21/**15**/34) → na reparatie 16/33/58/91 (17/25/33); bruin 61/95/130 (34/35, ok); crème 128/195/237 (**67**/42) → 153/195/237 (42/42) + lijn 100.
Clusters < 3 px: alleen omlijningsdiagonalen, oog/aftekening (bevroren), teenpixels en (29,33) (zie MAG).
