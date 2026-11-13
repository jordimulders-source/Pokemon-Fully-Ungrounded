# Eindkeuring Krassault `r3.png` (onafhankelijk, 13 nov)

Keurder tekende niets en las geen eerdere keuringen of makerlogs. Vel: `eindkeur_r3.png` (boven: 1×/2×/4× op licht en donker tussen Octillery, Tentacruel, Gyarados | Krassault | Kingdra, Scizor, Crawdaunt; midden: 8× licht, 8× donker, model; onder: simulatie van de reparatielijst en de lijnkaart). De simulatie is alleen een controle van de lijst, geen sprite.

**Oordeel in één zin:** technisch een nette, gesloten Gen 3-sprite die het model trouw volgt; nog niet af door 5 kleine afwerkfouten (8 + 5 pixels) en één paletkeuze. Na de MOET-lijst: **AF, zekerheid ±75%**.

## 1. Hoofdvraag: kan hij ertussen staan?
- **Ja qua tekenwerk, net niet qua waarde.** Lijnvoering, detailniveau en netheid passen bij Gyarados/Scizor/Crawdaunt. Wat als eerste stoort: op 1× en 2× is hij de donkerste en vlakste van de zeven. Gemiddelde luma 69 tegen 110–143 bij de referenties; aandeel pixels met luma < 50: 35% tegen 8–19,5%. De kleurfamilie is goedgekeurd en volgt het model (modelbasis 149,50,65 ≈ idx5), dus geen FAIL; de oorzaak die wél binnen de opdracht valt is de kleine stap schaduw → basis (zie 2c).
- **Leest op 1×/2×:** mantel + vin ja (sterkste deel); rechteroog ja (beste detail, leest op 1×); beide kanontentakels ja (zwarte loop + lichte rand); wratten ja (3 tinten, schaduw rechtsonder, consequent); rupsbanden op 2× ja, op 1× als twee donkere gestreepte blokken met gele stippen (voldoende).
- **Leest matig:** mondkanon op 1× (smelt met het donkere onderlijf, op 2× wel leesbaar als ring met gat); linker (verre) oog op 1×–2×: naast de wrat op x21 lezen het als drie gele streepjes in plaats van één oog.
- Naast het model: niets toegevoegd of weggelaten dat ik kan vinden; de reductie is trouw.

## 2. Dragonfly Cave / Gen 3, punt voor punt
**a. Omlijning: goed, 3 kleine fouten.**
- Gesloten: 314 randpixels, 173 idx1 + 130 idx2 + 11 geel (wratten). Geen open rode rand.
- 1 px: geen dubbele lijnen behalve één plek: (57–58,47) ligt direct op de lijn (54–59,48) → blok van 3×2 zwart.
- Lichtkant gekleurd, schaduwkant zwart: consequent. 0 pixels lijnrood aan de schaduwkant (rechts/onder); zwart links alleen waar het klopt (onderkant, schaduwzijde arm).
- "Nooit zwart en lijnrood om en om": 2 losse pixels: (51,8) idx2 midden in de zwarte vinrand; (7,48) idx2 in de zwarte onderrand.
- Lichte kleur op de buitenrand: (21,22) en (54,24) zijn idx11 (lichtgeel) op de rand; de andere 9 gele randpixels zijn idx10 (donkergeel) en dat is in orde (Octillery doet hetzelfde).
- Zwarte binnenlijnen: 218 px (waarvan ±40 in de lopen). Scizor en Crawdaunt hebben er ±200–210: geen afwijking. Bandlijnen naar idx2 getest in simulatie: banden worden rustiger maar verliezen het rupsbandkarakter; niet aanbevolen.

**b. Schaduw: goed.**
- Eén lichtbron linksboven, consequent op mantel, vin, wratten, banden. Geen pillow shading.
- Korrel: clusters < 3 px in middentinten: 115 (51 per 1000 px). Referenties: 75–161 per 1000. Krassault is dus schoner dan vijf van de zes. In rood (idx3–6) 42 kleine clusters, vrijwel allemaal op terechte plekken (kanonranden, tentakelpunten, ribbels, spiraalkern).
- Banding: één echte plek: schaduwstreep van 1 px op de linkerarm (13,33–35) met basis links ervan; in het model is die hele linkerzijde één schaduwvlak. Lichte banding: hooglichtband langs de linkermantelrand is 7 rijen exact 4 px breed (y17–23); volgt het model, MAG.
- Kanonranden (mond, rechterkanon) zijn rondom idx6: de rechter-onderzijde hoort een tint lager (MAG).

**c. Palet: binnen de norm, één zwakke stap.**
- 10 kleuren + transparant (max 15): ruim in orde.
- Rood: lijn idx2 + vulling 3/4/5/6 + glans 7 (8 px). Eén tint meer dan de norm (≤ 3 + omlijning); idx3 (77 px, alleen onder de banden) verschilt 13 luma van idx4 en is op 1× onzichtbaar: geen kwaad, geen winst.
- Luma: idx1 14 · idx2 35 · idx3 47 · idx4 60 · idx5 83 · idx6 128 · idx7 167. Stappen vulling: 4→5 = **23**, 5→6 = 45, 6→7 = 39. Norm ±30–40; Octillery 60/43/52, Scizor 39/41/69. De stap schaduw → basis is te klein: schaduwvlakken (onderlijf, armen) scheiden op 1× niet van de basis.
- Bijna-zwart (luma < 30): 17,5%. Referenties 8,0–19,5% (Scizor 18,1, Crawdaunt 19,5): binnen de band, bovenkant.
- Hooglicht idx6: 198 px = 14% van de rode vulling; aan de zuinige kant voor R/S, maar volgt het model.
- Geel 10/11/12: luma 128/193/229, goed.

**d. Leesbaarheid per onderdeel**
- Rechteroog: goed (lid zwart, schaduwrij in idx11, spleetpupil, geel vlak).
- Linkeroog (x23–25, y34–38): trouw aan het model (diagonale pupil), maar concurreert met wrat (21,32–33) op 1 px afstand.
- Mondkanon: ring + gat leesbaar op 2×; binnenwerk (idx4 in de loop) volgt het model.
- Rupsbanden: kappen met ringzuignappen lezen; spiraallijnen lezen op 4×.

## 3. Reparatielijst voor de laatste kleurronde (alles binnen het silhouet)
**MOET**
1. **Paletstap schaduw → basis** (0 pixels): idx5 van (160,48,64) naar ±(168,56,72), luma 83 → 91; stappen worden 31/37/39. Blijft in de goedgekeurde familie; in de simulatie op 1×/2× net wat meer vorm. Raakt Jordi's kleurkeuze: als A/B voorleggen.
2. **Dubbele lijn:** (57,47) en (58,47) idx1 → idx4.
3. **Losse lijnkleur:** (51,8) idx2 → idx1; (7,48) idx2 → idx1.
4. **Lichtgeel op de buitenrand:** (21,22) idx11 → idx10; (54,24) idx11 → idx10.
5. **Schaduwstreep linkerarm:** (11,33), (11,34), (12,34), (11,35), (12,35) idx5 → idx4 (wordt één schaduwvlak zoals in het model).

**MAG**
6. Wrat naast het linkeroog ondergeschikt maken: (21,32) idx12 → idx11; (21,33) idx11 → idx10.
7. Mondkanonrand rechtsonder: (26,44), (27,44), (26,45), (27,45) idx6 → idx5.
8. Rechterkanonrand schaduwzijde: (50,26), (51,26), (51,27) idx6 → idx5.
9. Wratrand aan de lichtkant: (8,32), (8,33), (8,34) idx1 → idx2.
10. Hooglichtband mantel laten taps lopen: (37,17) idx6 → idx5 (band 3 px bovenaan in plaats van 7 rijen precies 4).

**Niet doen:** bandlijnen lichter maken; vin of mantel anders schaduwen (volgt het model en leest).

## 4. Buiten de opdracht (silhouet staat vast, alleen ter kennis)
- Ingesloten gaatjes van 1 px: (8,43) en (9,44); spleten van 1 px breed: (45,36–37), (18,38–41). Ze zitten in het model; op een lichte achtergrond zijn het losse stipjes.
- Onderrand bij (19–20,60–61): trede van 2 px dik zwart.

## 5. Eindoordeel
- **Nu (r3): niet af**, door punten 2–5 (13 pixels) en de paletstap.
- **Na MOET 1–5: AF.** Zekerheid ±75%. Restrisico: (a) Jordi vindt hem op 1× nog te donker/vlak, ook met de paletstap; dat is dan een keuze over de kleurfamilie, niet over afwerking; (b) het linkeroog op 1× (punt 6 helpt, lost het niet helemaal op binnen het silhouet).
- Metingen: `ek_*.py` in de scratchpad van de keurder (niet in de repo); alle getallen hierboven komen daaruit.
