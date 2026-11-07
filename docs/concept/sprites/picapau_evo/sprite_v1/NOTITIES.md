# Picapau-evolutie: frontsprite v1 (maker)

Jordi (letterlijk): **"Ga een sprite bouwen. Dat is makkelijker aan te passen"**. Het model stopt bij C3 (`../blender/r3/`) en is niet meer aangepast. Methode Picapau sprite v2: kleur per spritepixel uit de render plus een labelkaart, cel voor cel overtrekken. Alleen de oren zijn opnieuw getekend (Gen 1, Jordi's hoofdbron). Grenzen voor de oren: "too much", "te wit, te groot".

## Bestanden
- `bron/renders.py` (Blender): `labels.png` (elk onderdeel een vlakke kleur, zelfde camera en kader als C3_8x: schaal 0,8896, schuif −3,81/−3,81) en `wit.png` (model wit, toonkaart).
- `bron/bron.py`: `bron_kleur_1x/8x.png`, `bron_labels.txt` (L lijf, B buik, K kop, W wang, U/I kuif, N snavel, V/F vleugel nabij/ver, S stip, T koord, Z bliksem, O oog, P poot), `bron_toon.txt` + `toonkaart_1x/8x.png` (4 tonen), `overtrekvel.png` (render | bron 8× met raster).
- `palet.py` (16 kleuren incl. transparant), `start.py` → `raster_start.txt` + `onderdelen.txt` (automatische eerste overtrek), `handwerk.py` → `raster.txt` (al het handwerk, per plek met reden), `bouw.py` → `picapau_evo.png` (geïndexeerd, 16 kleuren, index 0 transparant) + `normal.pal`.
- `controle.py` → `controle_uitvoer.txt`; `vel.py` → `vel.png` (1× en 8×: sprite, Picapau af, Raichu Gen 1, Taillow, C3-render); `kijk.py` is een hulp voor snelle kijkvellen.
- Draaien: `python3.11 start.py && python3.11 handwerk.py && python3.11 bouw.py && python3.11 controle.py && python3.11 vel.py`.

## Palet (Picapau naar kastanje en crème)
- **Omlijning en kastanje:** k zwart; 1/2/3 kastanje licht/basis/schaduw (2 = Celeus elegans, warm oranjebruin). 3 is ook de lichte tint van de vleugel.
- **Vleugel en koord:** v vleugelbasis en koord; 4 donker kastanje voor selout aan de lichtkant, binnenlijnen en de schaduw van vleugel en koord.
- **Crème:** a/b/e licht/basis/schaduw voor buik, stippen, snavel en de gedempte oor-binnenkant (b/e, niet wit).
- **Overig:** c wang; y/Y bliksem, met 1 (oranje) als bliksemschaduw en selout zoals bij Pikachu; w glans; g/G grijs voor de poten en de iris.

## Wat overgetrokken is en waar ik afweek ("dichter bij het model omdat...")
1. **Massa, kop, buik, lijf, vleugels en koord** komen uit de render. Het onderdeel komt uit de labelkaart, de tint per kleurgroep uit de toonkaart (3 licht, 2–1 basis, 0 schaduw). De omlijning is zwart aan de schaduwkant en selout aan de lichtkant.
2. **Oren:** opnieuw getekend naar Gen 1. Het zijn driehoeken met een brede basis op de kop, een kastanje rand en een gedempt lichte binnenkant (b met e onderaan). De punt loopt zelf smal door in een krul naar buiten en omlaag, als haak met een gaatje van 1 px; geen ring op een steeltje.
   - Het verre oor is dezelfde vorm gespiegeld, met de schaduw weer rechts.
   - Maat: rij 9–18, x 9–32, net zo hoog en breed als de C3-oren.
3. **Verre vleugel bovenaan:** links van x 30 en boven rij 14 weggelaten, zodat het verre oor vrij tegen de achtergrond staat (opdracht). Zijn kleur is basis v met alleen de donkerste toon als 4; de toonkaart maakte er een zwarte manen-vlek achter de kop van.
4. **Bliksem:** zelfde plek en lengte als in de render, maar met een duidelijke Gen 1-knik. De bovenste band is smal en loopt naar linksboven, de onderste band is breder en verspringt 3 px naar links. De render liet hier alleen een insnoering zien.
   - De randen per rij zijn links oranje selout 1 en rechts en onder zwart, zodat er geen om-en-om op één rand zit.
5. **Kop en lijf:**
   - Kop- en lijfrand rechts: de automatische binnenlijn was 2–4 px breed; alleen de pixel die echt aan de vleugel grenst is 4 gebleven, de rest is schaduw 3 (sikkel rechts).
   - Kop: licht alleen als ovaal linksboven, de rest basis 2. De toonkaart gaf een groot plat lichtvlak.
6. **Vleugelstippen:** vervangen door ronde sjablonen (2×2, 4×3 of 4×4) op het midden van de stip-labels uit de render. De render gaf blokjes en scherven; Picapau heeft ronde stippen. Op de verre vleugel zijn ze in b, wat afgeknipt was tot < 4 px is weer vleugel.
7. **Oog:** pixel voor pixel van Picapau (af), 4×4: glans linksboven, iris onder. Alleen het nabije oog, zoals in de render.
8. **Snavel:** met de hand beitelvormig, 9 px lang (x 7–17, rij 29–33), crème hoorn met selout e boven en zwart onder. Er is geen donkere onderkant die als open snavel leest.
9. **Pootjes:** klein en grijs; de verre poot staat hoger en is donkerder (perspectief). De render gaf hier alleen een vlek.
10. **Kleine opruimingen** (lijst in `handwerk.py` §6): de buikrand links is doorlopend e (geen k ertussen), de snavelrand doorlopend, een gaatje van 1 px tussen vleugel en lijf is dicht, en losse pixels gingen naar de omringende tint.

## Controle (`controle_uitvoer.txt`)
- **Rand en losse pixels:** geen lichte kleur op de buitenrand (de oranje bliksem-selout telt als gekleurde selout), geen losse pixels, geen pixels die alleen diagonaal verbonden zijn.
- **Tintclusters:** geen clusters < 3 px (8-verbonden; omlijning k/4 en oog/glans uitgezonderd).
- **Kleuren:** 15 kleuren + transparant, 1830 px.
- **Afwijking van de C3-massa:** 89 px buiten de massa en 70 px van de massa leeg gelaten. Dat zijn de opnieuw getekende oren, de bliksemknik, de snavel, de pootjes en de verlaagde verre vleugel; allemaal bewust (zie hierboven).

## Hoofdvraag (op 1×)
- **Wat leest:** een oranje-kastanje vogel met kop 3/4 naar links-voor (oog rechts in de kop, snavel naar links), twee Raichu-achtige oren met krul, een grote opgezette donkere vleugel met ronde stippen, en de donkere koord-S met de gele bliksem linksonder. Raichu herken je in oren, staart en bliksem; het blijft wel een specht door de snavel en de vleugel.
- **Imposant:** het frame is goed gevuld (1830 px tegen ±830 bij Picapau).

## Zwakke punten (eerlijk; hierom nog niet klaar voor Jordi zonder keuring)
1. **Schaduw is blokkerig, niet op Taillow- of Picapau-niveau.** Lijf, buik en kop hebben grote vlakke tintvlakken met getrapte grenzen. De buikgrens (crème naar kastanje) loopt in trapjes, en de buik heeft horizontale tintbanden (a boven, b, dan e onderaan), wat neigt naar banding. Dit moet een volgende ronde met de hand gladder: vloeiende sikkels die de vorm volgen.
2. **De wang** is één rood vlak (17 px) zonder tweede tint; er was geen paletplaats meer.
3. **Strook achter de kop:** tussen kop en nabije vleugel zit nog een donkere strook van 2–4 px. Dat is de verre vleugel, zoals in de render, maar op 1× leest hij als een donkere nek of manen.
4. **Snavel:** leest als een lichte wig, maar is vrij plat en bleek naast de kop; de basis heeft geen eigen schaduw.
5. **Pootjes:** grof (blokjes grijs, tenen nauwelijks); g staat als lichte selout op de rand.
6. **Bliksem:** de randen zijn nog trappig (diagonaal van ±1 px per rij), en het gele vlak is twee vlakke tinten met een horizontale overgang.
7. **Oren:** lezen als Raichu-oren. Bij het verre oor zijn de krul en het gaatje rommelig (k en 2 door elkaar), en de oren zijn op 1× net aan "katachtig" als je de krul mist.
8. **Vleugel:** veel donkere schaduw (4) in de onderste helft, waardoor hij zwaar oogt. De ronde stippen zijn netjes, maar staan in een vrij regelmatig raster.

Volgens de werkwijze: Claude kijkt op 8× naast Taillow, dan een verse keurder. Reparaties daarna via deze maker (`handwerk.py` per plek). Punt 1 (schaduw) is het belangrijkste.
