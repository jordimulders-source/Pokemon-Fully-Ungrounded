# Keuring welp p2, 15 nov

Onafhankelijke keurder, eerst blind: 8× naast r11 en het model (model op het spriteraster gelegd, ±16,9 px per spritepixel), 1× naast Seviper, Growlithe, Vulpix en de volwassen steenjaguar. Daarna p1/keuring.md nagelopen.
Palet = r11: 1 zwart, 2 donkerste bruin (lijn), 3/4/5 bruin donker/mid/licht, 6/7/8 lila donker/mid/licht, 9 crème-schaduw, 11 crème, 14 perzik.

## Oordeel: **FAIL** (dichtbij; twee vormfouten in de schouderspiraal)

### Gemeten
- Alpha-diff tegen r11 = 0; lijnpixels (1/2) ongewijzigd; diff 197 px, alleen in x 24–48, y 32–55 (lijfzone). Kop/oog (y < 30) identiek aan r11.
- Patroonpixels 241 (r11: 175): lichaam meer bedekt, schouderspiraal groter dan in het model (±12×13 px tegen ±9×10), zoals Jordi vroeg.

### Wat goed is
- Het zijn geen lijntjes meer: schouder en heup lezen als ingekleurd vlak (Jordi: "het moet meer een patroon op het lichaam gaan worden ... echt inkleuren"). Geen crème barsten, geen dikke belijning, lijf niet bol, silhouet onveranderd.
- Heupspiraal is opgeknapt: één crème band met groef in 3, lila boog rechts/onder, lila streepje linksboven zoals het model; geen losse korrels meer, leest als spiraal (geen schietschijf).
- Facetten op poten, borst (5 op x 21–24, y 40–42) en heupfacet (5, y 47) blijven staan.

### p1 MOET-punten
1. Oog terug: **opgelost** (diff y < 30 = 0).
2. Staart als één haak: **technisch opgelost** (doorlopend, 11 links / 9 rechts), maar de vorm die p1 voorschreef is een letter "J" geworden; zie MOET 1 hieronder.
3. Heup opschonen: **opgelost**.
4. Volume schouderschijf: **deels**; er staan een paar 7-pixels ((32,44), (32,45), (34,40), (34,41)), maar de schijf is nog grotendeels vlak 8 en de ring is rondom dicht, zodat het geheel een platte sticker blijft.

### MOET
1. **De haak leest als een losse "J" aan een lolly, niet als de krul van het model.** In het model loopt de crème boog van linksonder óver de top naar rechts en gaat aan de **rechterkant** (x ≈ 33–35) door naar beneden; onderaan krult hij naar links en weer **omhoog naar binnen** (een kleine spiraal, aan de ring vast). In p2 hangt een recht steeltje aan het **midden-onder** van een dichte ring ((30,49)–(31,52), voet (28,52), (28–30,53)) en loopt de voet alleen naar links: precies een J.
   - Steel naar rechts verplaatsen, aansluitend op de ring rechtsonder ((33,48)=11, (34,48)=9 blijven): (32,49)=11, (33,49)=9, (32,50)=11, (33,50)=9, (31,51)=11, (32,51)=9; krul: (30,52)=11, (29,51)=11, (29,50)=11, tip naar binnen (30,50)=9. Niet over de beenlijn op x 34 (index 2) heen.
   - Oude steel/voet terug naar de r11-basis (bruin 4/3 volgens `p1/basis.npy`): (30,49)–(30,52), (31,49)–(31,52), (28,52), (28,53), (29,53), (30,53).
   - Met de diff-tool na afloop tonen dat de krul aan de ring vastzit (geen bruine pixel tussen ring en steel).
2. **Ring onderaan open, zoals het model (geen schietschijf/donut).** Het model heeft aan de onderkant (tussen het linker eind van de crème boog en de steel) géén crème, maar de lila buitenwinding. Nu is de ring onderaan 2 rijen dik crème: y 47 x 28–34 (11) en y 48 x 28–32 (9). Maak (28,47)…(31,47) lila **7** (buitenwinding, schaduwkant) en (27,48)…(31,48) terug naar basisbruin (3/4 uit `basis.npy`); laat (32–34,47) en (33–35,48) crème als begin van de steel. Daarmee wordt de crème een C-boog die in de haak overgaat: één spiraal in plaats van ring + losse letter.
3. **Gat in de linker ringrand:** (26,43)=3 is een los bruin pixel in de crème ring (eronder (26,44)=11, erboven (26,42)=11). Maak het **11**. Dat is ruis die bij "blurry mess" hoort.

### MAG
- Rugkrul (einde lila rugstreep, x 37–40, y 37–41): in het model een duidelijke kleine spiraal; nu een 3×3 vlekje met donkere stip ((39,39)=3). Mag één winding groter als dat zonder hertekenen van de rugstreep kan (model op het raster leggen, niet verzinnen).
- Schijfvolume: na MOET 2 de onderste lila (rij y 45–46 binnen de ring) in 7 houden, bovenlinks 8, zodat het licht linksboven doorloopt; het brede 8-vlak (x 27–32, y 38–45) mag één extra 7-pixel aan de schaduwkant krijgen, geen nieuwe tinten.
- Heup: rij y 54 (7) boven rij y 55 (6) is licht banding-achtig; (41,55) en (46,55) mogen 3 worden zodat de 6 een taps eind krijgt.

### Hoofdvraag eigenaar
Zou Jordi dit mooi vinden en zou ik hem trots tonen? **Nog niet.** De richting is duidelijk beter dan r11 (ingekleurd patroon, meer bedekt, lijf en 3D van poten/borst intact), en de heup is goed. Maar op 1× springt de schouder eruit als een bleke **dichte ring met een stokje eronder** (lolly/doelwit + "J"), en dat is precies het element dat in het model het mooist is: één spiraal die in een krul overgaat. Met MOET 1–3 (samen ±25 pixels, allemaal binnen de patroonzone) verwacht ik een versie die je met vertrouwen kunt laten zien; daarna opnieuw laten keuren.
