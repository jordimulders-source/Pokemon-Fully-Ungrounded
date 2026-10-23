# Olinguito ronde 12: echt voorovergebogen, korte poten, haakklauwen, mond (basis ronde 11)

Jordi op ronde 11: "wederom een stap vooruit". Kleuren, masker/bandietenband, kop, ogen en de egale buik zijn behouden (palet ongewijzigd, kop pixel voor pixel gelijk op de mond na). Lijf, poten, armen en klauwen zijn opnieuw met de hand getekend (`bron/delen_abs.txt`).

## Bestudeerde sprites (zie compare.png, onderste rij)
- **Sandslash (Gen 3):** laag, compact lijf dat naar voren helt, korte poten met kleine voeten, klauwen die vanaf de poot naar voren en dan omlaag haken. Overgenomen: het lage, horizontale lijf met de kop vóór en onder de heuplijn, en de klauwrichting.
- **Zangoose (Gen 3):** de klauwen hangen in het verlengde van de onderarm en buigen naar de grond; de bolle kant zit voor/boven. Overgenomen: klauw = voortzetting van de pols, holle kant naar achteren-onder.
- **Golduck (Gen 3):** voorovergebogen; dichtbije been gebogen en naar voren, verre been anders van hoek en deels verborgen. Overgenomen: de twee achterpoten in duidelijk verschillende hoeken.
- **Sneasel en Grovyle (Gen 3):** het hele lijf is één diagonaal, het ene been draagt (gebogen), het andere strekt naar achteren (afzetten). Overgenomen: verre achterpoot gestrekt naar achteren-onder, dunner en in schaduw.
- **Drilbur, Obstagoon (de sprites die de repo heeft):** opgetrokken schouders, de kop laag en naar voren, armen als klauwwapen vóór het lijf. Overgenomen: opgetrokken verre sluippoot onder de kin, kop lager dan de rug.
- Ook bekeken: Zigzagoon, Poochyena, Meowth, Sentret (verre poten hoger en korter dan de dichtbije; voetjes klein en rond).

## Wat er veranderde (per feedbackpunt)
1. **Mond:** een kleine scheve grijns onder de snoet: vanaf de snoethoek een korte donkere lijn (omlijningsbruin) met een gat roomkleur tot de kaaklijn, de rechtermondhoek 1 px omhoog, en één wit hoektandje onder de lip. Klein en ondeugend, past bij Dark.
2. **Klauwen in de goede richting:** ronde 11 begon verticaal en boog aan de punt naar voren uit (helling 3-2-2-1-1): de holle kant zat voor-boven, dus gespiegeld. Nu omgekeerd: vanaf de vinger eerst 2 px naar voren, dan 1, 1, en de punt recht omlaag (verschuiving per rij −2, −1, −1, 0, 0, 0). De bolle kant zit voor/boven, de holle kant naar achteren/naar de grond, zoals Sandslash en Zangoose. Ze liggen in het verlengde van de onderarm (die ook naar voren-onder loopt), beginnen direct onder een vinger en de omlijning loopt door (8 links/boven, 0 rechts/onder). De achterste klauw is korter en anders gebogen (−1, −1, −1, 0, 0) dan de voorste, dus geen kopie. Lengte ±7 rijen (ronde 11: ±9, maar door de haak even lang langs de curve).
3. **Niet meer gelijnd:** de achterpoten verschillen in alles. Dichtbij: gebogen, knie naar voren, draagt het gewicht, voet onderaan (y55), lichtere tinten. Ver: gestrekt naar achteren-onder (afzetten), dunner, in schaduwtint (2/1), voet 1 rij hoger en kleiner (8 vs 9 px breed). De voorpoten staan op verschillende hoogtes: de verre opgetrokken onder de kin, de dichtbije lager en naar voren. Kop, schouder, heup en staart liggen niet meer onder elkaar.
4. **Echt voorovergebogen:** de kop zakte 5 px en schoof 5 px naar voren (bovenkant oor y22, was y17); het lijf ligt nu vrijwel horizontaal, met de heup als hoogste punt van de rug (y32) en de schouders onder de kin (±y40). De rug is een holle-bolle lijn: holte achter de kop, bolling over de heup, dan de romp omlaag naar de staart. Sluiphouding zoals een kat of Sandslash.
5. **Poten kleiner:** de achterpoten zijn ±11 rijen (ronde 11: ±14), de voeten 8–9 px breed (was 10), passend bij een compact boomdier. De klauwen aan de voorpoten bleven het kenmerk.
6. **3/4 naar links-voor:** kop ongewijzigd in 3/4 (verre wang en snoet links, blik naar de kijker); het lijf staat diagonaal: verre poten hoger/rechts en in schaduw, dichtbije poten lager en lichter.
- **Animatie:** frame 2 = kop, staart en beide armen 1 px omhoog (de klauwen worden even opgetild); lijf en achterpoten blijven staan. Onder de kop loopt het lijf 4–6 px door, zodat er in frame 2 geen gat of open rand ontstaat.

## §0-checklist (SPRITING.md)
1. **Lichaam én blik diagonaal:** ok. Kop in 3/4, lijf schuin: verre achterpoot en verre arm hoger, kleiner en in schaduw.
2. **Geteld en verbonden:** ok. 2 oren, 2 ogen, neus, mond (met tandje), 2 armen (elk met 2 klauwen), 2 achterpoten met tenen, 1 staart; alles sluit aan. bouw9: geen open randen in beide frames.
3. **Geen rechte lijnen:** ok op één na: de onderkant van de dichtbije elleboog loopt door in de buiklijn (5 px, y46). In frame 2 is de rechterkant van de romp 5 px recht waar de staart 1 px omhoog gaat.
4. **Ogen geïntegreerd:** ok (ongewijzigd uit ronde 11: in het masker, glans + donkergouden reflectie, verre oog kleiner en anders gebouwd).
5. **Silhouet op 1×:** lange pluimstaart omhoog, maskerkop vooraan, witte klauwen vóór en onder de kop; leest als een sluipend klein roofdier. Let op: het oogt nu meer viervoeter dan ronde 11 (zie hieronder).
6. **Formaat:** 1063 / 1075 px (ronde 11: 1026), 36 rijen hoog (was 41) maar breder (x9–59). Fase 1: Treecko 967, Mudkip 852, Torchic 782; door de lange staart iets groter, zoals eerder.
7. **Pose niet stijf:** ok. Gewicht op de dichtbije gebogen achterpoot, verre poot zet af, één voorpoot opgetrokken, de andere naar voren.

## Controle (bouw9)
- Open randen: geen (beide frames). Zwart-aandeel rand 0,59 (ronde 11: 0,62; doel 0,35–0,6: nu binnen).

## Voor Jordi
- De houding is nu bijna die van een sluipende viervoeter (kop laag, rug horizontaal). Als hij te veel kat/wezel wordt: kop 2 px omhoog en het lijf iets steiler (heup lager), dan zit hij tussen ronde 11 en 12 in.
- De verre sluippoot onder de kin is klein; op 1× lezen vooral zijn klauwtjes.
- De mond is bewust klein (Gen 3-kraalgezicht); als hij beter moet lezen kan het tandje 1 px langer of de grijns 1 px breder.

## Bestanden
- `anim_front.png`, `normal.pal` (palet = ronde 10/11), `compare.png` (boven: ronde 11 en 12, beide frames, 1× en 3×; onder: Sandslash, Sneasel, Grovyle, Golduck, Zangoose, Drilbur, Obstagoon).
- `bron/delen_abs.txt`: **de bron**, met de hand geschreven rijen `y x pixels` per deel (achter naar voor). Bouwen: `sh bron/bouw.sh <ronde12-map> [preview.png]`. `bron/vergelijk12.py <repo-root>` maakt compare.png.
