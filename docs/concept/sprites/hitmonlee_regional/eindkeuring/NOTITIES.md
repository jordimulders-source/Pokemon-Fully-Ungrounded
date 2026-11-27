# Eindkeuring 1 (ek1) – regionale Hitmonlee (glas, omhaal)

Keurder: onafhankelijke eindkeuring (schaduw + belijning + kleurtinten), 27 nov. Basis: `sprite/kandidaat.png` (= r13, figuur op x+2).
Bestanden: `ek1.png` (64×64, geïndexeerd, zelfde palet, 15 kleuren + index 0), `ek1_8x.png`, `vel.png` (kandidaat 8× | ek1 8× | model op dezelfde schaal; 1× licht/donker),
`ek1.py` (alle wijzigingen als lijst, met assert op de oude waarde), `ek1_log.txt` (per pixel; coördinaten in r13-raster en in 64×64).

## Oordeel
- **Eis 1, accuraat op het model: PASS** (na ek1). Pose, silhouet, ringen, voeten, oog, glanspunten en gloeiend hart volgen het model. Eén echte afwijking gevonden en hersteld: het doorschijnende kickbeen liep in het model zichtbaar (lichtbruin/crème) de romp in tot een ronde onderkant (rij 29–34); de r11-toonkaart had die pixels naar gloed-oranje/bleekroze gezet, waardoor het been in de romp wegviel. Teruggezet op de gemeten modeltint (M_gem = M_zonderlijn).
- **Eis 2, Gen 3: PASS met kanttekeningen** (zie Open).
  - Belijning: buitenlijn 1 px, donkerrood selout boven/links, zwart rechts/onder. Hersteld: één om-en-om-pixel op de bovenkant van de trapvoet, twee dubbele zwarte hoeken/randen (trapvoet rechtsboven, trapbeen rij 10, knie rij 42), zwarte binnenlijnen in de romp (schouderplooi) en in de nabije hand → donkerrood (binnenlijn = donkerste eigen tint, taps naar de zwarte onderlijn). Zwart binnenin blijft alleen bij de ogen, de lijn romp/kickbeen (rij 26–31), de romp boven de verre arm en de vingers van de verre (beschaduwde) hand.
  - Schaduw: volume zit erin (romp: bleekroze koepel met witte glans → rood → gloeiend geelwit hart; benen: ringen licht links/donker rechts bij het trapbeen); glas leest als glas (glanspunten op koepel, schouder, voet, oog en kickbeen; doorschijnend been nu ook in de romp).
  - Kleurtinten: 15 kleuren + transparant. Losse zwarte spikkel in de knie weg.

## Wijzigingen (23 px, silhouet 0 px veranderd)
- Belijning (11): (41,1) 1→2; (44,2) 1→6; (45,10) 1→5; (18,39) 1→3; (18,40) 1→2; (17,41) 1→2; (8,53) 1→2; (5,54) 1→2; (5,55) 1→2; (4,55) 1→2; (53,42) 1→13.
- Kleur/spikkel (1): (51,42) 1→13.
- Doorschijnend kickbeen in de romp (11): (36,29) 12→15; (35,30) 7→15; (39,31) 11→14; (36,32) 12→14; (39,32) 12→14; (40,32) 7→15; (35,33) 7→14; (36,33) 12→14; (37,33) 12→14; (39,33) 7→14; (37,34) 7→14.
Coördinaten = r13-raster (59 breed); in de 64×64 x+2. Elke nieuwe waarde = modelmeting (`sprite/M_gem.npy`/`M_zonderlijn.npy`), behalve (4,55): model D, 2 gekozen voor een doorlopende vingerlijn.

## Open (niet zelf gedaan, met reden)
1. **Ringen zijn ladderachtig met tintwissels binnen een band** (bv. rij 12 F8F83): dat zit zo in het model (glansstreep per ring), dus geen ruis van de maker. Strakker maken = interpreteren; laten staan, Jordi laten kijken.
2. **Standbeenringen lichter aan de rechterkant** (licht linksboven verwacht): volgt het model (gloed van binnenuit). Ter info.
3. **Linkerkant romp donker karmijn** terwijl het licht linksboven valt: modelkeuze (gloed van binnen, rand koelt af). Niet aangepast; groot vlak, geen kleine reparatie.
4. **Tinten per groep > 3** (gloed 5, rood glas 4): verloop van het hete hart; ruimte is er (15/16), geen banding-trapjes gezien. Ter info.
5. **Nabije schouderbol en vingertopbolletjes** lezen op 1× niet als aparte glasbolletjes (al door de maker genoemd): vergt vorm, niet tint; niet zonder tekenen op te lossen.
6. Kussentje trapvoet (4 tinten in 4×4) is druk maar leest op 1× als lichte stip zoals in het model.
