# Evo van Picapau, modelronde 3 (C3): alleen kuif en staart

Jordi over C2 (letterlijk): **"de oren en staart zijn geen raichu staart"** · correctie: **"nee de gen 1 raichu sprite moet je ook naar kijken"** → Gen 1 (`referenties/jordi_inspiratie_raichu_gen1.png`) is de hoofdbron, Gen 3 (`referenties/raichu_gen3_8x.png`) aanvulling. Eerdere grenzen voor de kuif: "vooral de oren zijn too much", "te wit, te groot".
Model `picapau_evo_r3.py` (kopie van r2; alleen kuif, staart en bliksem nieuw, plus de verre vleugel verschoven, zie onder). Draaien: `python3.11 maak_r3.py` → `C3_8x.png`, `C3_1x.png` (1812 px, hetzelfde kader als C2: schaal 0,890), `standen_r3.png` (Gen 1, Gen 3, C2, C3, Picapau), `closeup_r3.png` (8×: oren en staart van Gen 1, Gen 3 en C3, render en 1×).

## Wat ik tel in de bronnen (1× = 64 px)
**Gen 1 (hoofdbron)**
- **Staart:** zwart, **±4 px dik** (kolommen 59–63, rij 38–56). Komt rechts achter het lijf vandaan (x≈50, y≈33), gaat rechts tot de framerand en omlaag (y 38–56), dan onderlangs naar links (y 56–62, x 30–58), onder het lijf door.
- **Bliksem:** lang en schuin, van onder het midden (x≈30, y≈60) naar linksboven tot de framerand (x 0, y≈30). ±40 px lang, 8–10 px breed, lichte vulling met zwarte rand, één duidelijke verspringing (x 11–17, y 50–56). De staart omarmt het lijf en vult het frame.
- **Oren:** groot, met een lichte (roze-witte) binnenkant. Het rechteroor (x 47–63, y 2–25) eindigt in een spiraal van ±8 px doorsnee met een gat (x 53–63, y 14–25). Het linkeroor (x 26–48) heeft een omgeslagen, gekrulde punt.

**Gen 3 (aanvulling)**
- **Staart:** dunne koord van 1–2 px, donkergrijs, in een lus van ±14 × 12 px rechts achter het lijf.
- **Bliksem:** ±29 px hoog en ±16 px breed (bijna de helft van de spritehoogte), geel, scherpe hoeken, 2 knikken.
- **Oren:** driehoekig, ±7–10 px breed en ±8 px hoog, bruine buitenkant en gele binnenkant. Aan de punt van het rechteroor een dun spiraaltje van 1 px, ±5 px groot.

## Wat ik deed
- **Kuif = Raichu-oren (Gen 1-vorm, maat als C2):**
  - Per kant een platte driehoek (nieuwe prisma-SDF `plaat` met scherpe vorm), basis ±7 BU breed, top op ±28,5 (C2 ±30).
  - Buitenkant kastanje (lijfkleur), binnenkant gedempt licht oranje-crème (niet wit) met een kastanje rand.
  - Aan de punt een spiraal naar buiten (buis van 0,75 BU, straal 3,0 → 1,7, ruim een slag), tot ±13,5 BU opzij (C2 ±10).
- **Staart = Gen 1:**
  - Dikke donkerbruine koord (r 2,4 BU, op 1× 3–4 px) in een S: uit de stuit naar rechts, ver rechts omlaag (naast de vleugel zichtbaar), onderlangs naar links, achter de pootjes door.
  - Eindigt in een grote platte bliksem (prisma, scherpe hoeken, één verspringing), schuin naar linksboven tot de framerand, ±28 px lang. Gen 1 eindigt ook op de rand.
  - De bliksem staat in het beeldvlak van stand C (lijf 40). Hij is dus alleen voor C vlak; in een andere stand moet het vlak mee.
- **Verre vleugel** (alleen deze, meld ik hierbij): 5 BU naar achteren en 11 BU lager (`VERRE_VLEUGEL`), omdat de kuif er anders volledig tegenaan stond. De nabije vleugel en de rest van C2 zijn ongewijzigd: lijf, kop, kopdraai, snavel, kleuren, pose en kader.

## Leest het op 1×?
- **Bliksem: ja.** Groot, gele zigzag, overal ≥ 3 px behalve de uiterste punt (scherp, zoals bij Raichu).
- **Staart: ja.** Een donkere band van 3–4 px. De S is zichtbaar rechts naast het lijf en onderlangs, maar het eerste stuk (uit de stuit) verdwijnt achter de vleugel.
- **Oren: half.** Driehoek en lichte binnenkant lezen, en de spiralen zijn op 1× kleine ringen met een gat van 1–2 px.

## Eerlijk oordeel: leest het nu als Raichu?
- **Staart en bliksem: ja.** Dit is het duidelijkste Raichu-kenmerk van het model geworden: een donkere S onder het lijf met de lange bliksem linksonder, zoals Gen 1. Wel minder "omarmend" dan Gen 1: daar loopt de staart om een veel groter deel van het lijf en vult hij het frame meer.
- **Oren: deels.** De driehoek met lichte binnenkant en de spiraal verwijzen duidelijk naar Raichu.
  - Zwak: de spiraal zit als ringetje op een steeltje boven de driehoek, waardoor het van dichtbij op slakkenvoelsprieten lijkt. Bij Raichu loopt het oor zelf in de krul over.
  - Zwak: het verre oor staat ondanks de verschoven vleugel deels tegen de bruine vleugel, met weinig contrast.
  - Voorstel voor een volgende ronde: de oorpunt zelf laten omkrullen (de driehoek smal laten uitlopen in de spiraal) in plaats van een losse ring.
- De rest (lijf, vleugels, kleuren) heb ik niet beoordeeld; die zijn bevroren.
