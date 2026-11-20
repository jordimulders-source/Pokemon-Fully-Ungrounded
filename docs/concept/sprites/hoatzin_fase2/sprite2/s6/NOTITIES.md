# Hoatzin fase 2, ontwerp 2, s6 (20 nov): belijning kuif/snavel/poten + meer tinten en schaduw

Jordi: "het zit in de belijning van de kuif, snavel en poten. Daarnaast is er veel teveel effen kleuren, meer kleurtinten, meer schaduw".
`sh alles.sh` (bouw6.py + hand.json). Basis s5. Niets getekend: silhouet = s5 behalve 3 losse ruispixels (8,36),(11,36),(37,61) (script bewijst het); oog ongewijzigd.

## Palet (16, index 0 transparant)
1 lijn · 2-4 blauwzwart (112,114,166)/(70,72,118)/(48,46,80) (R2) · 5-7 creme (244,236,212)/(198,194,176)/(144,142,134); 6/7 zijn ook grijs licht/midden (snavel, poten) · 8 oogrood (bevroren) · 9-11 krop · 12-14 kuif (178,108,70)/(146,80,54)/(106,48,34) · 15 gezicht blauw.
Plekken: creme-schaduw en grijs zijn samengevoegd (bijna gelijk); grijs heeft daardoor licht/midden + de lijn als donkerste. Kuif-licht gedeeld met oogrood geprobeerd: oog werd oranje, verworpen.

## Wat er gebeurde
- **Omlijning (R1)** per onderdeel in bouw6.py: rand tegen lucht aan de schaduwkant (rechts/onder) zwart, aan de lichtkant de donkerste eigen tint; dunne delen (< 2-3 px) krijgen geen eigen lijn maar een donkere tint (anders worden plukken en tenen zwart).
- **3 tinten + sikkel** voor kuif, creme (nek, staartpunt), krop: licht linksboven, sikkel rechtsonder. Krop volgt de cel-shading van het model (onderlaag 6/7/8).
- **Hand (hand.json):** kuif (lichte band linksboven, donker onderaan boven de gezichtslijn), snavel (licht bovenop, midden, lijn onder), poten (licht links/boven, midden rechts/onder), staartpunt (R5: vlak licht, sikkel onderaan, (57,48) lijn).
- **R3** verre vleugel: losse 2-pixels -> 4, behalve de bovenrand. **R4** dubbele zwarte penlijnen 1 px. **R6** lijf: sikkel 4 van 2 px rechts/onder, lichte band 2 links.
- Diagonale 1-px-penlijnen op een vlak geven dambord: de pixel linksboven van de stap wordt een tint lichter (penrand). Daardoor 9 losse 3-pixels in de vleugels.

## Controle
dambord 0 · om-en-om 0 · klonten 0 · barcode 0; losse tintpixels 21 (9 penrandjes, klauwen/teentoppen, staartveren).
Afwijking van s5 (zelfde rol, paletverschuiving niet geteld): kuif 38, snavel 25, nek 41, krop 32, verre vleugel 25, nabije vleugel 10, lijf 64, staart 18, poten 24 (228).
`naast.png`: s5 | s6 | Honchkrow, Staraptor, Mandibuzz, pitahaya fase 3 op 1x/2x. `vel.png`: s6 | s5 | model, kop 12x.

## Eerlijk
- Strakker dan s5 (kop en poten lezen nu als omlijnde vormen, vleugels lichter met meer contrast), maar Honchkrow/Staraptor hebben nog grotere, rustiger vlakken met een harder licht. De verre vleugel is nu bijna vlak donker.
- Grijs mist een eigen donkere tint (paletruimte); snavel en poten gebruiken de lijn als schaduw.
