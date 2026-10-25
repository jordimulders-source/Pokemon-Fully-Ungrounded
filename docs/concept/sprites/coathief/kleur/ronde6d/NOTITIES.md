# Coathief: kleursprite ronde 6d (afwerking van de overlap van de voorpoten, en de voorpoten iets dikker)

Basis: ronde 6c. Jordi's lijn staat in 6c (`lijn.py`). Jordi over 6c: "het sluit nog niet helemaal perfect aan. Kijk naar de non sprite [...] moet iets betere afwerking". Aanvulling: "in het origineel zijn de voorpoten ook ietsje dikker".

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `onderlaag_6b_6c_6d_voorpoten.png`: de voorpoten op 8×, met de onderlaag, 6b, 6c en 6d naast elkaar, op licht en op donker, plus de hele sprite op 1×.
- **Nieuw silhouet:** `../../silhouet/ronde5.txt` (1326 px, 5 px meer dan ronde4). De overlay op de onderlaag staat in `../../silhouet/overlay_ronde5.png`; de nieuwe pixels zijn rood. Het script is `bron/silhouet_ronde5.py`.
- `bron/`:
  - het blok "ronde 6d" staat onderaan `reparaties.txt`. 6c veranderde alleen pixels die 6d volledig overschrijft;
  - `diff_r6c.py` is de diff tegen 6c;
  - `bouw.py` en `controle.py` werken met `silhouet/ronde5.txt`.

## Bewijs
```
controle.py: pixels 1326 | silhouet 1326 (ronde5.txt) | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r6c.py:
zone overlap voorpoten (x 17-33, y 48-58)          31 px
zone verdikking buiten die zone (x 15-34, y 48-61)   2 px
totaal 33 | buiten de zones: 0
```
Dat is binnen het budget van ±60. De 5 silhouetpixels zijn meegeteld.

## Verdikking (silhouet, +5 px)
- **Manchet van de opgetilde poot:**
  - (26,54): ronder naar rechts; de inkeping (lucht) tussen de poten begint nu op y 55, zoals op de onderlaag;
  - (25,56): ronde onderkant rechts.
- **Staande poot:**
  - (32,54): bovenkant 1 px breder onder de curve;
  - (31,58): pols 5 px in plaats van 4;
  - (31,59): enkel.
- Er blijft lucht tussen de poten (26,55–56) en tussen de klauwparen. De klauwvormen zijn ongewijzigd.

## Afwerking van de overlap
- **Bruine bovenarm (vacht):** een ronde V die uit de borst komt (y 50–53, rij 50 x 26–31 → rij 53 x 28–29).
  - lichtkant l linksboven, b in het midden, d als schaduw langs de curve;
  - zoals op de onderlaag (bruin van y 50 tot de punt bij y 54).
- **Eén doorlopende k-curve** van de buik omlaag langs de elleboog: (31,49), (32,50–51), (31,52), (30,53), dan horizontaal (29–27,54) als onderkant van de arm. Daarna loopt hij als ronde onderkant van de manchet door: (26,54) m, (25,55), (25–24,56).
  - De segmenten lopen geleidelijk van verticaal naar horizontaal (2, 1, 1, 3), zonder hoek of trap.
  - Jordi's lijn is 1 px naar rechts verschoven, naar de bruin/verre-poot-grens van de onderlaag.
- **Gebogen naad** tussen de bruine arm en de donkere manchet: (25,50), (26,51), (27,52) en (27,53) in m aan de kant van de manchet, met d of l aan de kant van de arm.
- **Manchet:** donker en rond, in de nabije tinten, met Y/y-licht linksboven, z, en m en k onderaan.
- **Verre poot** onder de curve:
  - eerst slagschaduw m: (31,53), (30,54) en (27–28,55);
  - daarna de schaduwtinten met de lichtkant (y) vanaf y 56;
  - een knik bij de pols op y 57–58.

## Toets (1× en 8×, licht en donker)
- De nabije poot (bruine bovenarm, donkere manchet, hangende klauwen) ligt zichtbaar vóór en over de verre poot, die eronder uitkomt.
- De curve is één vloeiende lijn. Op 1× zie je twee voorpoten, de nabije voorop.
- Het geheel volgt de onderlaag.
- Ik zie geen zwak punt.

## Les
- Een lijn van Jordi is een richting, geen pixelvoorschrift. Lees de onderlaag eronder af: welk vlak (vacht, manchet of verre poot) ligt waar.
- Teken daarna de omlijning als één curve met geleidelijke segmenten, en zet de slagschaduw direct eronder.
