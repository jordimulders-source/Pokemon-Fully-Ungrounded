# Ronde 15 kleur (maker) — notities
Basis: ronde 14 (`../ronde14_kleur/`) met Jordi's bijsturing van 7 nov: geen brede snavelplaat, rond oog, muil ±175 px, minder origami. `r5.py` schrijft alle 62 rijen opnieuw met de hand, elke rij als één string van de linker tot de rechter omtrekpixel. Dat de rijen even lang zijn als in de basis is per rij gecontroleerd, en de alpha-diff met `basis_85.txt` is 0. Er is geen randpixel rechtgetrokken.
Palet: zoals in ronde 14. Index C (muil licht) wordt niet meer gebruikt: de muil heeft 3 paarstinten (9/A/B) plus de lip D.

## Wat er gedaan is
- **Muil: 177 px** (9/A/B/D, waarvan 3 px keelspleet in index 1 binnen de muil niet meegeteld). In ronde 14 was dat 137.
  - De mondlijnen zijn muil geworden: de bovenste mondlijn is nu de donkere rand (9). Langs de wangkant schuift de grens 1 px naar buiten: een 9-rand met een lichte lip D erbuiten. De mondhoek is 1 px groter. Op (14,25), (14,26) en (15,27) staat nu lip in plaats van een dubbele buitenlijn. De zwarte randjes langs het haakje zijn muil geworden.
  - Onder het oog laat ik 2 px lichte veren (6) staan, want de mondlijn op (19–20,14) is daar gezicht gebleven.
- **Dieptewerking zonder banding:** het dak onder de snavel is donker (9 en A), de keel is het donkerst, met een spleet achterin. Licht valt alleen als een sikkel (B) op de kaakbodem, langs de verre lip. De overgangen zijn onregelmatig breed.
- **Snavel:** het haakje is niet vergroot. Er staat alleen een lichte snavelrug (6) op x11–12 y10, en het haakje is lichter (7) zodat het tegen het donkere dak loskomt.
- **Oog:** een ronde schijf van 5×5 met afgeronde hoeken op x19–23, y8–12, puur zwart. De wenkbrauwschaduw is weg.
- **Halsrand:** een schaduwband van 2 px (4, de laatste wangpixel plus de oude lijn), met lichtere veren (5) erachter.
- **Opschonen:** het eilandje bij de kin is buitenlijn of kinschaduw geworden, de losse pixel op (18,29) is weg en de kaakpunt is één ronde punt. De schorsvlekjes zijn groepjes van 3 px in L-vorm.
- **Lijf:**
  - De borst heeft een gebogen glans langs de linkerrand in plaats van het witte blok, plus drie kleine schubgroepjes.
  - De vleugel en rug zijn donkerder (3/F) dan de borst. Op de vleugel staan twee schubranden van dekveren, en drie pennen met ronde punten op verschillende hoogte (y47, y52, y56) met schaduw onder de punten. Onder de tak heeft de vleugel geen doorlopende lijn meer.
  - De staart heeft een lichte linkerkant, losse gebogen bandjes en schorsvlekken.
  - De buikband (2) op y41–43 is de takschaduw.

## Zelf nog zwak
- **Vleugel:** nog origami. De penlijnen lopen recht en evenwijdig van y33 tot de punten, en de schouderrand loopt in een rechte diagonaal. Zachter zou zijn: lijnen die licht buigen en eerder ophouden, en meer tussentonen.
- **Muil:** het donkere 9-vlak is groot en egaal; op 1× leest het als een diep gat met een lichte onderlip. Dat is wel de bedoeling, maar het dak heeft weinig vorm.
- **Haakje:** op 1× klein, en de hoornkleur (7) is dezelfde als die van de schorsvlekjes.
- **Schorsvlekjes:** de grijsbruine vlekjes op nek en staart lezen als vuil.
- **Halsrand:** leest als een rechte band, niet als een rafelige kraag.
- **Controlescript:** 47 kleurclusters kleiner dan 3 px, vooral diagonale lippen, de randen en de penpunten.
- Niet blind getest.
