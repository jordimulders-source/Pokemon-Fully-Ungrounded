# Keuring r4 – Octillery-evolutie frontsprite (`octi.png`)

Onafhankelijke keurder, 11 nov. Eerst blind geoordeeld met eigen vergrotingen (1×, 2×, 8× en 14× met coördinaten). Het model `referenties/ontwerp_gekozen.png` (bbox 148–1002 × 41–596) is geschaald naar de sprite-bbox (1,24)–(62,63) en op hetzelfde raster gelegd. Ter vergelijking: Gen 3 Octillery, Gyarados en Seviper (`anim_front_gba.png`, bovenste frame). Getoetst zijn alleen (1) trouw aan het model en (2) een goede Gen 3-sprite. Coördinaten zijn spritepixels (x,y).

## Eindoordeel: NOG NIET klaar voor Jordi (bijna)

r4 is een grote stap vooruit ten opzichte van r3.
- Het aandeel bijna-zwart (index 1 en F) is gedaald van 36% naar 21%.
- Binnenlijnen zijn nu donkerrood.
- De tentakel rechtsboven is een echte boog met een spitse punt.
- Het gezicht leest: twee ogen met een boos lid, een lichte kinbult en een mondkanon met ribbels.
- Op 1× en 2× leest hij als een rode inktvis met twee kanonnen.

Er staat nog één echte afwijking van het model in, en de punt van de onderste tentakel rechts is nog stomp. Met één kleine reparatieronde (punt 1 t/m 3, bij voorkeur ook 4 en 5) is hij klaar. Dat hoeft dan geen volledige nieuwe keuring te zijn: een pixeldiff buiten de zones plus een blik op 1×/2× is genoeg.

Helderheid (gemiddeld 84,5, het model zit op ±88) is volgens afspraak geen punt.

## Per onderdeel

| Onderdeel | Oordeel |
|---|---|
| Mantel, segmentlijnen, rugvin, staartvin | GOED, op de onderrand na (punt 3) |
| Kop, kinbult (33–37, 51–54) | GOED |
| Ogen (ver 26–28/40–41, nabij 35–40/40–42 met lid 33–37) | GOED |
| Krul achter de kop met 2 wratten | GOED |
| Mondkanon (opening 20–23/45–50, ribbels 24–31) | GOED, klein punt 6 |
| Bovenste kanon (monding 3–4/40–42) en arm | GOED |
| Onderste kanon (monding 9–13/54–59), wratten links ervan | GOED |
| Tentakel rechtsboven met zuignappen binnenkant | GOED |
| Donkere boog met zuignappen (toegestane toevoeging) | GOED |
| Tentakel rechts midden (40–62, 50–53) | REPAREREN (punt 2) |
| Rupsband-lus onderaan | REPAREREN (punt 1, 4, 5) |
| Roze schijven linksonder (24–29, 60–62) | GOED, staan zo in het model |
| Wratten onder de kin weg, naden weg (toegestane afwijkingen) | GOED |

## Reparaties, op belang

1. **Roze schijven rechtsonder weghalen (trouw, verplicht).**
   - Het gaat om de pixels (41–43, 60–61) en (46–48, 59–60), in de kleuren 7, 8 en 9.
   - In het model staat daar de donkerrode buik van de rupsband-lus: tint 3, onderste rij tint 2, zonder schijven en zonder geel.
   - De enige roze schijven in het model zitten linksonder bij x=22–31, y=58–63, en die staan in de sprite goed.
   - De gebogen binnenlijn in tint 2, van (34,60) via (40,59) en (46,58) naar (50,57), moet blijven. Onder die lijn tot aan de buitenlijn: 3, met 2 aan de onderkant.
2. **Punt van de tentakel rechts midden (trouw + vorm).**
   - Nu loopt de tentakel van x=44 tot 62 als een band van 3 px met een stompe punt (x=59–62, y=51–53, onderrand `1111` op y=53).
   - In het model loopt hij licht omhoog, wordt hij dunner en krult de punt omhoog naar ±(62,49).
   - Opdracht: maak x=56–62 taps van 3 naar 1 px. De bovenrand blijft op y=50/51, de onderrand stijgt van y=53 naar y=51. Eindig in een spitse punt op (61–62, 49–50).
   - De zuignappen (53,53) en (57,53) blijven aan de onderkant.
3. **Onderrand van de mantel is nog vlak.**
   - Nu staat er op y=37 een rechte lijn van 10 px (x=51–60, index 1).
   - In het model daalt de rand van ±(58,36) naar ±(49,38).
   - Opdracht: laat de rand over die lengte 1–2 px schuin aflopen naar links. De rest van de mantel blijft ongewijzigd.
4. **Rechte F-kolom in de rupsband.**
   - Op x=30, y=58–62 staat een verticale lijn van 5 px in F.
   - In het model is dat een gebogen lijn van de opgerolde lus, met de holle kant naar rechts.
   - Opdracht: laat de lijn buigen, bijvoorbeeld (31,57) → (30,58–59) → (30,60) → (31,61–62), en teken hem in tint 2 in plaats van F. Het is een binnenlijn.
5. **Gele wratten op de rupsband (klein).**
   - In de sprite staan er 2, op (35,58) en (37,59).
   - Het model heeft er 3 op de bovenrand van de lus, net onder het einde van de loop: ±(31,57), (33,58) en (35,58).
   - Opdracht: verschuif ze ±2 px naar links en voeg de derde toe.
6. **Rechte kolom tussen de ribbels en het gezicht (klein, optioneel).**
   - Op x=32, y=44–51 staat een verticale lijn van 8 px in tint 2.
   - In het model is dat de ronde achterrand van het geribbelde kanon.
   - Opdracht: laat de lijn 1 px uitbuigen, met het midden (y=47–48) op x=33.
7. **Onderrand rechts (optioneel).** Tussen x=40 en 52 ligt de onderrand ±1 px lager dan in het model, dat bij x=40 op ±y=61,5 zit en bij x=48 op ±59,5. Pas dit alleen aan als het meekomt met punt 1.

## Wat goed is (bevriezen, diff 0)

- Alles buiten de zones hierboven.
- In het bijzonder: beide kanonnen met hun mondingen, het mondkanon, de krul, beide ogen met lid, de kinbult, de tentakel rechtsboven, de donkere boog met zuignappen, de roze schijven linksonder, het palet en de compositie (bbox 62×40, verhouding zoals het model).
