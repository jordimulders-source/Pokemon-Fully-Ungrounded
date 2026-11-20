# Hoatzin fase 2, r4 (19 nov), maker

Reparaties op de keuring van r3 (6 punten). Alles opnieuw: `sh alles.sh`. `vel.png` = r4 | r3 | model | Pidgeot, 1×/2×, kop 12×. Buikvarianten opnieuw op r4: `buik/` (zelfde 4 paletten, pixels identiek). Meetgereedschap: `px.py x1 x2 y1 y2` (modelhelderheid per spritepixel, canvascoördinaten; `PC=85` voor percentiel) en `pxz.py` (zone-aandeel per pixel).

## Wat er anders is (gemeten, niets getekend)
1. **Binnenvlak nabije vleugel (x30–48, y22–36)**: gemeten met px.py: het model is daar donker (gemiddeld 33–55, ook p85 40–60; lichte schachten heeft het model in de onderste pennen niet, alleen in de bovenste rijen). Daarom: toon per cel = mediaan van de modelpixels zonder lijnen/strepen (in plaats van één toon per pen), zwarte pengrenzen in donkere pennen alleen waar het model < 38 is én doorlopend ≥ 3 px; tint 2 iets lichter gezet (#402A3C, model ±45–55) zodat het geen bijna-zwart blok meer is. Het 112112-patroon is weg. Waar het model middentoon is (y20–25), staat middentoon.
2. **Snavel**: snavelcellen (zone S/K in het snavelvak) per cel uit de modelmeting: rand en snavelspleet (p15 < 30) zwart, middentoon donkergrijs, ≥ 95 glans. Haakpunt omlaag tot (7,27) zoals het model; buitenlijn rondom zwart (geen grijs meer op de rand).
3. **Kuif**: lichte strengdelen alleen als doorlopende lijn ≥ 3 px; losse lichte spikkels (o.a. (13,12), (16–17,13), (15,14)) → donkerbruin. De onderste kuifmassa is volgens `pxz.py C` in het model 90–100 % bruin; daar blijft hij dicht.
4. **Linkerrand buik**: selout is nu mauve #5A3E52 (donkerder dan de buikschaduw), het lichte vlak loopt tot tegen de rand.
5. **Buik**: tonen uit de gladde modeltoonkaart (hooglicht ≥ 122 = de lichtvlek van het model, schaduw < 100 = nekoverlap boven en wingschaduw rechts) in plaats van de ellipsregel van r3.
6. **Rand achter het blauwe gezicht**: niet-gezichtcellen die het blauw raken in x14–17, y19–23 → zwart (6 px).

## Afwijkingen t.o.v. de onderlaag (stap A), per zone
| Zone | px | afwijkend |
|---|---|---|
| lijf/vleugel (M) | 891 | 418 |
| vleugelstrepen (W) | 178 | 155 |
| kuif (C) | 124 | 21 |
| gezicht (F) | 27 | 11 |
| oog (E) | 7 | 3 |
| snavel (S) | 15 | 9 |
| buik (P) | 161 | 38 |
| poten (T) | 73 | 30 |
| staart (D) | 120 | 33 |
| modellijn (K) | 219 | 108 |
| buiten silhouet | – | 3 |
| **totaal** | 1815 | 829 (silhouet 3) |
Per regel: `r4.log`.

## Resterende twijfels
- Punt 1: de keurder vroeg middentoon en donker alleen als sikkel; de meting zegt dat het model daar echt donker is (± 45–55). Ik heb de meting gevolgd; de armpennen zijn nu een rustig donker pruimvlak met enkele doorlopende pengrenzen. Als Jordi/Claude ze lichter wil, is dat een kleurkeuze (tint 2 of de drempel in `kies`).
- Buik bovenrand (y37): de meting geeft daar één rij middentoon onder de nek (model 100–112) boven de lichtvlek (135–143); dat blijft een vrij rechte rij.
- De snavel is vrij donker (model 75–100, tint 14 = 75) met één glanspixel.
