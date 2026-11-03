# Kolibrie pre-evo – maker3, silhouet ronde 1 (3/4-pose, 3 nov)

Opdracht: nieuw silhouet in driekwart. Jordi: "hebben we nog steeds geen driekwart pose"; "de vorm van de buik links [niet mooi]"; "we hebben expres een kleinere snavel gekozen"; "misschien snavel open omdat die gevoed wil worden. Moet echt cute zijn".
Bron: foto 5 (`jordi_5_uitvlieger_hand.webp`), gespiegeld zodat hij naar links kijkt. Houding getoetst aan Taillow en Starly (alleen houding, niets geknipt).

## Werkwijze
- Overtrekvel met 64-raster (`overtrekvel.py`, 7,5 foto-px per spritepixel; kruin en borst links van foto en silhouet vallen samen). Rij voor rij met de hand getekend als spans (`rijen.txt` → `silhouet.txt`), geen ellipsen, buizen of verkleinde vormen.
- 15 tussenstanden bekeken op 8× en 3×/1× naast Taillow en Starly. De belangrijkste stappen:
  1. Bek als twee dunne sprieten → las als snorharen. Daarna een 2 px dikke bek met punten van 1 px.
  2. De bek begon aan de linkerrand van de kop (profiel). Nu zit de basis ín de kop en steekt de bek maar 4–5 px uit, met een voorhoofdinkeping: 3/4.
  3. Het lijf was smal en liep rechtsonder als een rechte schuine lijn weg. Op de foto liep ik zo de rugmassa mis. Nu heeft het een volle, bolle rug zoals op de foto, maar lager dan de kruin.
  4. Op 875 px was hij te groot naast de eindvorm (±1000 px). Daarom heb ik alles opnieuw en kleiner getekend.

## Per zone (zie `overtrekvel.png`, oranje A–F)
- **Kop:** rond, kruin y15, kin y30. Kop is 47% van de hoogte (16 van 34 rijen), kopoppervlak 33% (limiet ±41%). Een nekinkeping op (34,21) maakt de kop een eigen onderdeel aan de rugkant. Aan de voorkant zit een kleine kininkeping (x16, y29–30).
- **A, bek:** kort en open bedelbekje, schuin naar links-voor. Bovensnavel 2 px dik met de punt (10,20). Ondersnavel 2 px dik met de punt (11,24). De gaap is 2–3 rijen; de mondhoek is gevuld op (14,22–23). Hij steekt 4–5 px voorbij de kop uit. Zo zie je de bek in perspectief en niet in profiel. Op foto 5 is de snavel lang en dicht: dat wijkt bewust af (foto 3 + Jordi).
- **B:** de vleugelpunten die op de foto als oren omhoog steken, zijn weggelaten (eerdere les).
- **C, rug:** op de foto zie je de rug van boven, op dezelfde hoogte als de kruin. Ik heb de camera lager gezet, op ooghoogte zoals bij Taillow en Starly. Daardoor zakt de rug tot ±y21–24, achter de kop, met een kleine bult (de nabije vleugelschouder). Rugcurve: 38-39-40-41-41-42-42-42-43…, bol, zonder rechte schuine lijn.
- **D:** de vleugelpunten liggen langs het lijf naar achteren. De punt steekt rechtsonder over het staartje uit (47,42; taps, 1 px). Daarmee wijst het lijf naar rechtsachter terwijl de kop naar de kijker draait.
- **E, borst en buik links:** één gelijkmatige bol zonder trap of deuk. De linkerrand loopt 15-15-15-16-16-15-14-14-13×5-14-14-15-15-16-17-19. De borst steekt 1–2 px voorbij het gezicht naar voren (Taillow heeft ook 5 rijen recht op de top van de borstcurve).
- **F, onderkant:** de camera staat lager, dus buik en pootjes komen in beeld; op de foto verdwijnen die in de hand. Het nabije pootje staat links en lager en heeft 2 teentjes. Het verre pootje staat rechts, 1 rij korter, en zit deels achter de buik. Tussen de pootjes zit 3 px lucht. De onderlijn loopt schuin op naar rechts (de verre kant ligt hoger).

## Telling
- **823 px**, box 38×34 (x10–47, y15–48), 0 gaten. Ter vergelijking: Taillow 838 (40×36), Starly 767 (34×39), het oude profiel r2 732 (38×37).
- 823 px ligt net boven de richtlijn ±650–800. De vorm is compact en bol, en ik heb bewust niet dunner getekend om onder 800 te blijven. Het verschil met de eindvorm (±1000 px) zit vooral in de bouw: de eindvorm is slank en langgerekt.

## Controle (zelf, 1× en 3× naast Taillow, Starly, Pidgey, Natu, Fletchling en het oude profiel; `vel.png`)
- **3/4 of profiel?** Ik zie een rond vogeltje dat schuin naar links-voor zit. De kop staat op de bolle borst, het lijf wijkt naar rechtsachter, de vleugelpunt wijst rechtsonder en de twee pootjes staan uit elkaar. Dat is dezelfde opbouw als Taillow en Starly. Het oude profiel (lange schuine romp, bek ver vooruit) is er duidelijk anders naast.
- SPRITING §0: 1 diagonaal 3/4 ok · 2 alles geteld en verbonden (bek, kop, lijf, vleugelpunt, 2 pootjes) ok · 3 geen rechte lijnen buiten de toppen van curven ok · 4 ogen: komen in de kleurronde, vlak boven en achter de bekbasis (±x19–21, y19–21) · 5 leest op 1× als jong vogeltje ok · 6 formaat zie telling · 7 niet stijf: pootjes verschillend en de onderlijn schuin ok.
- Checklist D: D1 binnen de band voor fase 1 (700–950) ok · D2 kop 47% ok · D3 compacte romp grotendeels achter en onder de kop ok · D4 breedte 38 ≤ 48 ok.
- Wat het silhouet zelf niet kan dragen en in de kleurronde moet komen: oog in het voorste derde van de kop, de nabije vleugel als plaat over de flank, en de gaap in perspectief (gele mondhoek). Dat is geen zwak punt van het silhouet, maar wel de volgorde.

## Bestanden
- `silhouet.txt`, `silhouet_1x.png` (`render.py`), `rijen.txt` (de spans zoals ik ze tekende)
- `overtrekvel.png` (`overtrekvel.py`, `zones.txt`)
- `vel.png` (`vel.py`)

## Lessen
- Bij een foto van boven (uitvlieger in de hand) neemt de rug de hoogte van de kruin in. Voor een Gen 3-camera zet je de rug lager achter de kop en laat je borst en pootjes eronder zien. Markeer dat als bewuste afwijking op het overtrekvel en houd de breedte en de bolle rugmassa van de foto aan.
- 3/4 in een silhouet van een vogel: de bekbasis zit binnen de kop (voorhoofdinkeping) en de bek steekt maar 4–5 px uit, voorbij de borst naar voren. Een bek aan de buitenrand van de kop leest als profiel.
- Een bek van 1 px dikke sprieten leest als snorharen. Teken elke snavelhelft 2 px dik met een punt van 1 px.
