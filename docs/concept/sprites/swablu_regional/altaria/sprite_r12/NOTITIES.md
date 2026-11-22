# Onweerswolk-Altaria frontsprite, ronde 12: kop + hals 2 px naar rechts (vanaf r11A)

Jordi (21 nov): "a is perfect, zou je alleen het hele hoofd + nek 2 pixels naar rechts kunnen schuiven en mij dan een vergelijking kunnen laten zien?"

Bouwen vanuit `altaria/`: `python3 sprite_r12/bouw.py > sprite_r12/vulpixels.txt && python3 sprite_r12/vergelijk.py`.
Bestanden: `altaria_r12_K1.png` (kuif blijft staan), `altaria_r12_K2.png` (kuif schuift mee), `_8x` van beide (wit), `vergelijking.png` (r11A | K1 | K2 op 8×, koppen 16× (X14–39, Y4–31), 1× op wit/crème/grijsblauw/zwart), `bouw.py`, `laag.py` (de laag), `vergelijk.py`, `vulpixels.txt` (elke vulpixel met kleur en herkomst).

## De laag (pixels verplaatst, niets hertekend)
- **Kop:** precies de kop van r11A (`sprite_r11/bouw.py`, variant A, 165 px), inclusief snuit/pluis, ogen en kinrand.
- **Hals:** de violette pixels onder de kop (Y≥30) die eraan vastzitten (78 px).
- **Halsrand:** de wolk-selout direct links van de hals (8 px, X22–23 Y32 en verder naar beneden).
- **K2** neemt daarnaast de hele kuif mee (violet boven Y17 en de streng over de rechtervleugel, Y≤21 X≥34).
- Alles 2 px naar rechts. Rechts valt de laag over de wolk heen. Buiten de laag, de nieuwe plek en de vulpixels: diff 0 met r11A (assert).

## Vulpixels (wat links vrijkomt; volledige lijst in `vulpixels.txt`)
Regel: (1) had r9 daar wolk (die later door de grotere kop bedekt werd), dan precies die bevroren r9-wolkpixel. Een selout daaruit is de randlijn die doorloopt: (19,23). (2) Had r9 daar lucht, dan lucht. (3) Anders de eerste niet-laagpixel links: lucht of de vleugelrand (selout, koprijen) → lucht; in de halsrijen de wolkvultint van de dichtstbijzijnde wolkpixel links in dezelfde rij.
- **K1, 46 px:**
  - kop links-boven, lucht (11): (23–24,18) (21–22,19) (20–21,20) (20–21,21) (19–20,22) (20,23). Bij (19–20,22) en (20,23) staat nu een lucht-inham tussen de vleugelrand en de kop.
  - kop links-onder, r9-wolk (13): (19,23) S, (18,24) t, (19,24) n, (17–18,25) t, (17–18,26) d, (18–19,27) d, (19,28) n, (20,28) d, (20–21,29) d.
  - hals, band links (22): (24–25,30) n, (24–25,31) n, (22–23,32–34) t, (21–22,35–36) t, (20–21,37–38) t, (22–23,39) t, (23–24,40) d.
- **K2, 113 px:** dezelfde 46, plus 67 kuifpixels. Bijna allemaal lucht (de kuif stond tegen de lucht). In de vleugel: (49,20) c en (52,20) t (band links in dezelfde rij), waar de streng over de vleugel lag.

## Kuif
- **K1:** de stengels (Y17, X24–30) sluiten nog aan. De bovenrand van de kop ligt nu op X25–32; X25–30 staan er recht op, X24 diagonaal op (25,18). De kuif staat wel 2 px links van het midden van de schedel.
- **K2:** kuif en kop staan weer zoals in r11A ten opzichte van elkaar. De rechterstreng ligt nu 2 px verder over de vleugel.

## Controle
Beide: 14 kleuren incl. transparant, zwart alleen de 5 pupilpixels, alpha alleen veranderd in de vulpixels (lucht) en de nieuwe plek van de laag. Diff met r11A: K1 213 px, K2 417 px.
