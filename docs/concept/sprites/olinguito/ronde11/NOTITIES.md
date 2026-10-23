# Olinguito ronde 11: dynamische sluiphouding (basis ronde 10)

Feedback van Jordi op ronde 10 verwerkt. Kleuren (palet ongewijzigd), masker/bandietenband, staart en kop zijn gebleven; lijf, armen, klauwen en poten zijn opnieuw met de hand getekend.

## Wat er veranderde
- **Ogen diagonaal** (feedback 2): het dichtbije oog is 4×4 (was 3×4) met de pupil (2×3) in het midden en onderaan, iris links, rechts en boven; glans linksboven in de pupil, donkergouden reflectie rechtsonder. Het verre oog (3×3) heeft de pupil aan de kant van de kijker en is geen kopie van het dichtbije. In ronde 10 lag de pupil tegen de voorrand van het oog (= zijwaarts kijken); nu kijkt hij schuin naar voren, naar de kijker. Omlijning naast de pupil in maskerbruin (1) in plaats van zwart, zodat pupil en rand niet samensmelten.
- **Klauwen groeien uit de vingers** (feedback 3): de poot eindigt in een vingerrij (`13203220`, een zwarte splitsing tussen twee vingers) en elke klauw begint direct onder een vinger, met dezelfde breedte; de omlijning van poot en klauw loopt door. Lengte ±9–10 px (ronde 10: ±11). Elke klauw is één doorlopende haak met helling 3-2-2-1-1 (geen rechte stukken, punt alleen aan het eind) en sluit rechtsonder met zwart (geen open rand meer).
- **Hand minder bol** (feedback 4): de ronde vuist (10×11) is vervangen door een gebogen arm (schouder → elleboog naar achteren → onderarm naar voren) met een platte poot van 8×3.
- **Dynamische pose** (feedback 5): gewicht op het voorste been, dat naar voren en licht gebogen staat (voet x22–31, onderste rij y57); het achterste been staat naar achteren (voet x35–44, 1 px hoger). De verre arm is een **opgetrokken sluippoot** voor de flank met hangende klauwen (inbreker-houding), met een zwarte bovenrand en een rij basistint zodat hij op het donkere lijf leest. Alle vier de ledematen zijn zichtbaar en verbonden.
- **Lijf dunner en voorovergebogen** (feedback 6): ±16–17 px breed (was 20); de borst zit vooraan onder de kop en de rug loopt schuin naar de heup rechtsonder, waar de staart aansluit.
- **Buikcirkel weg** (feedback 7): geen crèmevlak meer. De onderkant is alleen iets lichter: een gekartelde band basistint (3) langs de borst/buik, overlopend in de schaduwtint (2), zoals de egale vacht van een echte olinguito.
- **Animatie:** frame 2 = kop, staart en voorste arm 1 px omhoog (ademhalen/oprichten); poten, lijf en sluippoot blijven staan.

## §0-checklist (SPRITING.md)
1. **Diagonaal 3/4:** lijf leunt naar links-voor, kop in 3/4 (verre wang en snoet links), blik naar de kijker; nergens zuiver profiel.
2. **Geteld en verbonden:** 2 oren, 2 ogen, neus, mond/snuit, 2 armen (elk met 2 klauwen), 2 benen met tenen, 1 staart; alles sluit aan op lijf of kop. bouw9 meldt geen open randen.
3. **Geen rechte lijnen in ronde omtrek:** bouw9 meldt nog drie stukken van 5–6 px: de pols/klauwlijn links en rechts (x14 en x21, y42–46; bewust: de lijn van poot naar klauw loopt door) en het kruis tussen de benen (y49, grotendeels verborgen). In frame 2 ook de achterkant van het achterbeen (5 px).
4. **Ogen geïntegreerd:** in het masker, omlijning deels in maskerbruin, glans + gekleurde reflectie; verre oog kleiner en anders gebouwd (3×3 vs 4×4).
5. **Silhouet op 1×:** snoet, oren, lange pluimstaart en de witte klauwen vooraan lezen op 1× (zie compare.png, bovenste rij).
6. **Formaat:** 1026 / 1042 px (ronde 10: 1050), 41 hoog. Fase-1-starters: Treecko 967, Mudkip 852, Torchic 782; door de lange staart iets groter, zoals eerder.
7. **Pose niet stijf:** gewichtsverschuiving, één been voor, armen asymmetrisch (de ene reikt naar voren, de andere opgetrokken).

## Controle (bouw9)
- Open randen: geen. Zwart-aandeel rand 0,62 (ronde 10: 0,61; doel 0,35–0,6, nog steeds iets hoog door het donkere lijf).

## Zelf nog niet tevreden over / voor Jordi
- Het lijf is nu slank; samen met de lange arm kan hij iets **minder knuffelig** ogen dan ronde 10. Als het te slungelig is: lijf 1–2 px breder of de voorste arm 1–2 px korter.
- De sluippoot is klein; op 1× lezen vooral zijn klauwen.

## Bestanden
- `anim_front.png`, `normal.pal` (palet = ronde 10), `compare.png` (ronde 10 en 11, beide frames, 1× en 3×).
- `bron/delen_abs.txt`: **de bron**, met de hand geschreven rijen `y x pixels` in doekcoördinaten (per deel, achter naar voor).
- `bron/abs2delen.py` zet die om naar `bron/delen.txt`; `bron/bouw9.py` (ongewijzigd) bouwt en controleert. Alles in één keer: `sh bron/bouw.sh <ronde11-map> [preview.png]`.
- `bron/vergelijk11.py <olinguito-map>` maakt compare.png; `bron/raster_f1.txt`/`raster_f2.txt` zijn de uitgeschreven frames.
