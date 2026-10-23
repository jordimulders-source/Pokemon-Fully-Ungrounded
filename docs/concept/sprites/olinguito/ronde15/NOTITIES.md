# Olinguito ronde 15: lijf als pixel-over op een echt Gen 3-skelet (Poochyena)

Jordi op ronde 14: "Hij blijft er onnatuurlijk uitzien. De rechterpoot mag meer staan, minder in beweging zijn [...]. Het lichaam blijft een onnatuurlijk geometrisch symbool en is niet netjes gevormd." Extra: het lijf mag **kleiner** (minder massa t.o.v. kop en staart) en **geleidelijker** gevormd (borst → buik → lies → dij zonder knikken of plotselinge stappen).

Andere aanpak: geen eigen constructie (boon/ovalen) meer, maar het lijf van een echte sprite als onderlaag. Alleen `been_achter`, `lijf` en `been_voor` in `bron/delen_abs.txt` zijn nieuw; kop, masker, ogen, mond, palet, staart, armen en klauwen zijn pixel voor pixel ronde 14 (gecontroleerd met diff; `normal.pal` identiek).

## Gekozen skelet: Poochyena
- **Waarom:** staat stil (alle poten op de grond, geen stap), in 3/4 naar links-voor, laag en compact, korte poten, kleine romp t.o.v. de kop. Precies de verhouding van een kleine boommarter met een grote maskerkop. Mightyena is te hoog op de poten, Persian loopt (één voorpoot in de lucht), Zigzagoon is een vachtbal zonder leesbare romp, Eevee/Skitty/Meowth zitten of staan rechtop, Absol staat op lange poten.
- **Onderlaag:** romp en achterpoot van Poochyena frame 1, **niet geschaald**, verschoven +0,+5 (zodat de achtervoet op de grondlijn van de olinguito komt). Kop, voorpoten, staartpluim en nekkraag weggelaten (`bron/onderlaag.py`). Zie `skelet.png`: referentie, onderlaag (rood) onder de olinguito, overtekening met de omtrek van de onderlaag, resultaat.
- **Overgetekend met de hand** (rijen in `delen_abs.txt`), aangepast aan de olinguito: gladde rug zonder vachtpieken, compacter, kleinere voet (8 px incl. omlijning, tenen als in ronde 14).

## Wat er veranderde
1. **Romp kleiner:** x24–53 / y32–48 (ronde 14: x24–57 / y32–49). Oppervlak 1049 px (ronde 14: 1096).
2. **Rug:** de nek dipt 1 rij achter de kop (y33), dan een lage boog over de heup (top y32, 4 px breed), naar achteren afgerond met horizontale runs 4,3,2,2,1 en verticale runs 2,4,3 (x52/53/52) die overgaan in de dij. Geen verticale kont meer.
3. **Buiklijn:** borst laagst (y48) direct achter de klauwarm, dan via runs 4,4,3,2 omhoog naar de lies (y45), die tegen de voorkant van de dij aansluit. Geen S met grote sprongen meer zoals ronde 14.
4. **Dichtbije achterpoot (rechts):** de Poochyena-poot: dij vormt het onderste deel van de ronde achterkant, de poot staat **recht onder de heup** (x43–48, verticaal), voet plat op y54. Eén houding, geen stap.
5. **Verre achterpoot:** links van en hoger dan de dichtbije (voet y52), in schaduwtint, bovenkant achter de buik; staat ook stil.
6. **Schaduw:** licht van linksboven: hooglichtband over de rug (y33–35), basis over de flank, schaduw onder de kop, op buik en achterkant; dij met eigen hooglicht linksboven en een lichte naad bovenaan.
- Animatie ongewijzigd (kop, staart, armen 1 px omhoog in frame 2; lijf en achterpoten staan).

## §0-checklist (SPRITING.md)
1. **Lichaam én blik diagonaal:** ok. Kop 3/4 ongewijzigd; het lijf erft de 3/4-stand van Poochyena (romp loopt naar rechtsboven de diepte in, verre achterpoot links-hoger in schaduw).
2. **Geteld en verbonden:** ok. 2 oren, 2 ogen, neus, mond, 2 voorpoten met elk 2 klauwen, 2 achterpoten met tenen, 1 staart; elke poot hangt onder zijn schouder of heup. bouw9: geen open randen in beide frames (een eerste versie had er een op (26,47) in frame 2, onder de opschuivende arm; opgelost).
3. **Geen rechte lijnen:** ok. bouw9 meldt geen rechte randstukken > 4 px (eerste versie: rugtop 5, borstonderkant 6, kont 8; alle drie gladgestreken).
4. **Ogen geïntegreerd:** ok (ongewijzigd).
5. **Silhouet op 1×:** ok; maskerkop, klauwen, pluimstaart en een kleine, staande romp op vier poten. Leest als een klein roofdiertje dat stilstaat, niet als een sprong.
6. **Formaat:** 1049 / 1065 px (ronde 14: 1096 / 1113). Bewust iets kleiner op Jordi's verzoek; fase 1 Treecko 967, Mudkip 852, Torchic 782 (verschil door de staart).
7. **Pose niet stijf:** ok; voorovergebogen kop, één voorpoot opgetrokken, klauwarm vooruit; achterpoten staan stil maar op verschillende hoogtes (diepte).

## Controle (bouw9)
- Open randen: geen. Rechte randstukken > 4 px: geen. Zwart-aandeel rand 0,59 / 0,58 (doel 0,35–0,6).

## Lessen
- **Een eigen constructie (ovalen, boon) blijft geometrisch lezen, hoe glad de pixels ook zijn;** het lijf van een echte sprite als onderlaag (`onderlaag.py`, niet geschaald) geeft in één ronde een natuurlijke romp en een consequente, staande pootstand.
- **Kies het skelet op houding én verhouding, niet op soort:** Poochyena (stil, laag, kleine romp, korte poten) past beter bij een kleine marter dan Mightyena (te hoog) of Persian (loopt).
- **Neem van de onderlaag de anatomie, niet de vacht:** staartpluim en nekkraag weglaten in het masker, anders tekent de overtrek vachtpieken als rugvorm.
- **Run-lengtes vooraf uitschrijven per curve** (bijv. rug 4,3,2,2,1; buik 4,4,3,2; kont 2,4,3) en daarna de rijen tekenen: zo zie je knikken vóór het bouwen en blijft bouw9 schoon.
- **Een romp die onder een bewegende arm doorloopt, krijgt op de verborgen randpixel al de omlijning** (hier (26,47) = 0), anders verschijnt in frame 2 een open rand.

## Bestanden
- `anim_front.png`, `normal.pal` (= ronde 14), `skelet.png` (referentie, onderlaag, overtekening + omtrek onderlaag, resultaat; 4× en 1×), `compare.png` (ronde 14 en 15, beide frames, naast Poochyena; 3× en 1×).
- `bron/delen_abs.txt` is de bron. Bouwen: `sh bron/bouw.sh <ronde15-map> [preview.png]`. `python3 bron/onderlaag.py <repo-root> 0 5` print de onderlaag als rijen; `python3 bron/skelet.py <repo-root> <ronde15-map> <uit.png> 0 5` maakt skelet.png; `python3 bron/vergelijk15.py <repo-root>` maakt compare.png.
