# Nachtaap fase 3: kleurronde 1i (5 nov), laatste kleine stap op 1h

Basis: `../ronde1h/` (blijft staan). Bron: `bron/ronde1i.txt` → `bron/bouw.py`; `bron/check.py` (bevroren delen t.o.v. v7, diff t.o.v. 1h); `bron/vel.py` (1i naast 1h).
Budget ≤ 20 px. **Totaal: 11 px diff met 1h, 0 px buitenomtrek.** Al het andere is 0 px diff met 1h.

## Per punt
1. **Buik (9 px):** de grens licht/schaduw is een boog geworden in plaats van een regelmatige trap.
   - De eerste S-pixel per rij 39–44 ligt nu op x45, 44, 43, 41, 38, 34. De stappen worden geleidelijk groter (1-1-2-3-4): steil bij de heup, vlak onder de buik.
   - Zo volgt de schaduw de buikronding, met de schaduw rechtsonder.
   - Gewijzigd van S naar V: (41–42,41), (38–40,42), (36–37,43), (32–33,44).
2. **Staartwortel (2 px, aan de heupkant):** (43,38) en (44,39) zijn van V naar S gegaan. De wortel waaiert daardoor schuin uit in de heup, zodat hij eruit groeit in plaats van erop te liggen. De wortel zelf (x≥44, rij ≤38) is 0 px veranderd.
   - Een echte tussentint tussen V en S heeft het palet niet. De overgang zit daarom in de vorm (een schuine aanzet) in plaats van in een extra kleur.

## Controle
- Bevroren t.o.v. v7: alles 0 px diff, behalve de eerder goedgekeurde (29,29), (30,30) en (29,30), en de armpixel (21,47) uit 1g.
- Open randen: 0.
- Losse pixels: geen nieuwe.
- korrel.py: 0 uitsteeksels, 27 inkepingen, 1 tand. Gelijk aan v7, 1g en 1h.
- Pixels: 1821.

## Eerlijk (alleen wat op 1× of 3× leest)
- Op 3× leest de buik ronder dan in 1h. De staartwortel sluit nu als één vorm aan op de heup.
- Op 1× is het verschil met 1h klein. Ik zie daar niets nieuws dat misleest.
- Het lijf als geheel is lichter en minder contrastrijk dan de render van het model. Dat komt door het palet: het is geen vormfout, en ik heb het niet aangepast.

## Lessen
- Een overgang tussen twee tinten kan ook zonder extra paletkleur: laat de vorm schuin uitwaaieren (fillet) in plaats van een tussentint te maken.
