# Poedelmot: kleur r8 (maker, zuinig)

Gebouwd vanaf r7 (r7 ongewijzigd). Nieuwe laag `stappen/k_r8.py`; de rest is bevroren. Maatstaven (Jordi): heel accuraat op het model, en een nette Gen 3-sprite.

## Gedaan
1. **Vleugelvlak** weer licht crème (`9`). Wit bovenaan, 2 px wit langs de rechterrand en een wit randje langs de kop. De tan voet (`6`) zit alleen vlak bij de kop.
2. **Krulmotieven**: elf halve boogjes van 1 px, met de hand op plekken uit het model gezet (middelpunt, straal en boog per krul in `k_r8.py`).
   - Voorvleugel: één grote krul plus drie rijen van twee langs de geschulpte rand.
   - Achtervleugel: vier krullen.
   - Bij de vleugelvoet `5`, verder `6`.
   - De krullijnen staan in `krul_lijnen.txt`; de controle telt ze als lijnwerk.
3. **Buik**: drie losse tan plaatjes (`7` bovenaan, verder `6`) met lichte gebogen naden (`9`) ertussen.

## Controle
- Alpha-diff 0. Open randen 0 (uitzonderingen: klauwtjes, sprietpunt).
- Selout zonder afwisseling. Losse pixels 0, clusters < 3 px 0.
- Donker-aandeel 0,222.

## Zwakke punten (8× naast het model)
- **Krullen**: kleiner en hoekiger dan in het model. Op 64 px zijn bogen met een straal van 2–3 px trapjes. Een paar lezen als "C"/haakje.
- **Buiknaden**: lezen op 8× als twee korte rechte streepjes ("="); in het model zijn het bollere plaatjes.
- **Sprietribben en pluimonderkant**: ongewijzigd ten opzichte van r7.
