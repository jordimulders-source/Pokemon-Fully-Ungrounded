# Ronde 16 kleur (maker) — notities
Basis: ronde 15. `r6.py` schrijft alle rijen opnieuw met de hand, elke rij als één string van de linker tot de rechter omtrekpixel. Bij elke rij is gecontroleerd dat hij precies tussen de omtrekpixels valt, en de alpha-diff met de basis is 0.

**Muil: 176 px** (9/A/B/D). Daarnaast staat er een keelgat van 7 px in index 1.

**Palet** (normal.pal, 16 kleuren):
- Index 7 (hoorn van het haakje) is warmer en lichter: 184,152,120.
- Index C is nu de tint van de schorsvlekjes: koel grijsbruin, 130,116,124. Het haakje houdt zo zijn eigen kleur.
- De muil gebruikt 9, A en B plus lip D.

## Wat er gedaan is (in de volgorde van de opdracht)
1. **Muil:**
   - De keelstreep is weg. In de plaats zit een rond keelgat in 1 op (20,18) en (19–21,19–20), met 9 eromheen.
   - De lichte bodem (B) is één massa linksonder (x14–19, y21–27) met een bolle bovenrand.
   - In y15–20 loopt de linkerrand direct van D naar A en dan naar 9.
   - Er ligt een slagschaduw van 1 px (4) langs de mondtop, op y14 x19–24, y15 x26, y16 x27 en y17 x28.
   - Om de 175 te halen is de mondhoek 1 px groter gemaakt, op (25,15), (26,16) en (27,17).
2. **Oog:** het felwit onder het oog is nu 5. Er zijn borstelveertjes bijgekomen vóór het oog (tint 4) en boven het oog (tint 5). Het oog zelf is ongewijzigd.
3. **Halsrand:** een gebogen kraag in 3/4 van 2–3 px, die links op y30–31 begint en rechts oploopt naar y28–29. Er zitten kartels (4) in de borst. Rechts loopt hij door tot de mantel- en vleugelgrens, zodat het een ring wordt.
4. **Onderlichaam:**
   - De penlijnen krommen licht, zijn twee keer onderbroken en lopen naar de staartpunt toe, met punten op y47, y52 en y56.
   - De buik is onderaan afgerond.
   - Er is een teenhint op (26–27,43), (27,44) en (29–30,43).
5. **Kop en mantel:** het 5-vlak is groter en 4 is een smalle sikkel. 3 komt alleen nog tegen de rechter buitenlijn voor. Er zijn 5 schorsvlekjes van 3 px in C (kop, mantel, nek en twee op de staart). De oude grijsbruine streepjes zijn weg.

## Zelf nog zwak
- **Vleugel:** nog blokkig. De lijnen lopen bijna recht, en de schouderrand is een lange diagonaal.
- **Bodem van de muil:** de lichte bodem kan als tong lezen.
- **Keelgat:** het is een klein koepeltje van 7 px en valt op 1× nauwelijks op.
- **Borstelveertjes en tenen:** op 1× bijna onzichtbaar.
- **Kop:** de 3-pixels langs de rechter buitenlijn vormen een trap van losse pixels.
- **Spikkels:** alle 5 hebben dezelfde L-vorm.
- **Controlescript:** 61 kleurclusters kleiner dan 3 px. Het gaat vooral om diagonale lippen, de 3-rand van de kop, kraagkartels en penpunten.
- Niet blind getest.
