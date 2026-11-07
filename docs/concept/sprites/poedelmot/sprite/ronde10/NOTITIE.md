# Poedelmot sprite ronde 10 (6 nov): Jordi's rode vormen zijn grenzen, vanuit ronde 9

Jordi (letterlijk):
- "ik bedoel dat ik cirkels heb getekend met de vraag of je daar binnen wil blijven en aan de rechterkant ga je vervolgens nog veel verder erbuiten. Waarom ben ik in hemelsnaam dan schetsen aan het maken?"
- "en ik bedoel daar is de ruimte waar je in kan proberen te werken".

Ronde 9 las de vormen verkeerd, als "vul dit erbij". Ze zijn de ruimte waarbinnen de poten moeten blijven.

## Masker (`masker.py`, `masker_*.txt`)
- Ik gebruik dezelfde overlay als in ronde 9: schaal 10×, verschuiving (-9, -51).
- Elke rode streepgroep heb ik dichtgetrokken tot zijn convexe omhulsel. De twee U-lussen in het midden tellen samen als één vorm.
- Daarna heb ik 1 px speling toegevoegd, omdat het schetsen zijn.
- Resultaat, in spritecoördinaten:
  - **links (kruis):** x9-14, y45-52;
  - **midden (U's):** x21-32, y50-58;
  - **rechts (lange lus):** x34-41, y41-57. Op y42-43 is hij maar x37-39 breed en op y57 alleen x37-38.

## Wat er gedaan is
- **Rechts:** alles in de pootzone buiten de lus is weg: het achterlijf dat naar rechts doorliep, R1 en zijn klauwtjes. De vleugel is gebleven.
  - Het gat tussen arm en vleugel heb ik buiten de lus teruggezet zoals in ronde 8 (open). Binnen de lus staat alleen de bovenrand van S (y44).
  - S loopt binnen de lus van onder de vleugel achter de rechterarm omlaag. De lus loopt onderaan maar tot y57 en is daar 2 px breed, dus S eindigt op y55 met een punt en zijn 2 klauwtjes staan op y56.
- **Midden:** de vulling tussen de voorpoten valt binnen de U's.
  - De onderrand van de buik heb ik op (23-24, 52) teruggezet zoals in ronde 6 (zwarte lijn). Die 2 px liggen net links van de U. Het is lijfrand en geen poot, dus ik tel ze apart.
- **Links:** de linkerrand loopt van de borst (x17, y39-40) via x17 (y41-43) en x16 (y44-51) naar de linkervoorpoot (x16, y52). Er staat niets links van die lijn.
- **Voorpoten:** ongewijzigd ten opzichte van ronde 6.

## Meting (`controle.txt`)
- rechts: **0** pootpixels buiten de lus;
- midden: **0** pootpixels buiten de U's, plus de 2 px buikrand uit ronde 6 die apart staan;
- links: **0** pixels voorbij de lijn, en 0 kruiscellen op het lijf;
- voorpoten: 0 gewijzigd;
- 118 px diff tegen ronde 9; 0 lichte pixels op de buitenrand, 0 ingesloten gaten, 13 kleuren.
- `paneel.png`: schets over ronde 9, schets over ronde 10, het masker (geel) over ronde 10 en ronde 10 los, alle op 8×, plus de onderkant op 16×. Het paneel staat ook onder in `keurvel.png`.

## Zwakke punten (eerlijk)
1. **S rechts:** op y45-50 is er tussen de armomlijning (x39) en de buitenrand (x41) maar 1 px wol (x40). De poot leest daar als een smalle strook achter de arm. Breder kan niet binnen de lus.
2. **Links:** de linkerrand is een rechte lijn op x16 van 8 px (y44-51). Er is geen bult, maar het lijf oogt links smaller.
3. **Midden:** de vulling tussen de voorpoten is één donkere wolmassa met een punt en 2 klauwtjes. Op 1× leest dat meer als schaduw dan als een poot.
4. Er is nog geen onafhankelijke keurder geweest.
