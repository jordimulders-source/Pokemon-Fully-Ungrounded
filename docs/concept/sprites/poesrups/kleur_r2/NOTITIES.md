# Poesrups: kleur r2 (benoemde reparaties op r1)

Start: `../kleur_r1/stappen/r1c.txt`. Handrasters: `stappen/r2.txt` → `r2b` (rijfouten 53–54, lokpunten, zachtere rechterkant krullen) → `r2c` (holtes onder de haakjes van krul 3–5, oogglans los van de lok) → `r2d` (bovenranden van de kam in 4; **eindstand** = `raster.txt`).

## Gemeten (nu ook kwart.py, lijnkaart.py en ov.py; alle drie getest en gebruikt)
- **Kam** (`kwart.py 14 28 31 40` en `30 33 48 48`, plus `fijn` op 32×): elke pluk is een lob die schuin oploopt naar een knobbel aan de rechterkant; de punt krult naar links met een donker haakje eronder; rechts een verticale zwarte lijn tot in de oksel. Model telt 6 plukken; alle 6 gehouden.
  - krul 1: top x19,25–22 op y29; haak (18,75–20; 30,0–30,5); lucht onder de haak tot y31,5; rechterlijn x22,5–23,25.
  - krul 2: top x27–28,75 op y31,25; haak (26,6–27,6; 31,6–32,5); lobrand y32,6; rechterlijn x29–29,5.
  - krul 3: top (34,3–35,3; 34,2); haak (34–34,4; 34,6–35,4); rechterlijn x36–36,3.
  - krul 4: top (39–39,8; 37,2); haak (39–39,3; 37,3–38,3); wit (39,5–40,5); rechterlijn x40,5–41.
  - krul 5: top (42,8–43,6; 41,2); rechterlijn x44,2–44,5. Krul 6: bultje (44–47; 45,9–47,5).
- **Pony** (`ov.py 4 46 34 63`): wit loopt door tot y54–55; lokpunten bij x7, 9, 12,5, 16, 19,6/21; donkere spleten bij x≈10, 15, 22; gezichtszone alleen y55–58,5. In r1 lagen de haarlijnen goed (kolom 9, 15, 22) maar zat er een band van 6 tussen wit en gezicht.
- **Verre oog**: zwart x9,8–11,3, y55–56,4 (gem. (10,55) 47, (10,56) 48); buitenlijn op (7,55)/(8,56). Het model toont het dus echt, met ±1,5 px gezicht ervoor.
- **Palet**: modelschaduw (200,192,168) en gezicht (168,152,128): R−B 32–40; larve 24–30. Meetbaar geler.

## Wat is veranderd
1. **Kam.** Krul 1: punt hangt 2 px naar links over met lucht eronder, wit in de steel (2 px), rechterkant in selout. Krul 2: lip (26,31) boven een open holte. Krul 3–5: lip naar links met een holte van 1–2 px eronder, witte kern, donker stipje (2) onder de lip. Krul 6: bultje. Bovenranden van de hele kam in 4 (model: grijs ±150), rechterkant 3, alleen de onderste okselpixel 2.
2. **Pony.** Lokken wit tot rij 53–55 met punten op (7,52), (8,54), (12,55), (15–17,53), (20,55); spleten kolom 9, 14/15, 18, 21/22 taps van 7/6 naar 4/3; gezicht direct 5 onder het wit (geen band van 6 meer).
3. **Onderrand/staart.** Lokken als lijn (4) met schaduwpixel (5) rechts ervan: (30,52)→(34,58), (35,53)→(38,58), (40,53)→(46,57), en in de staart (46,54)→(51,56) en (50,54)→(54,55), die uitkomen op de trapjes van de onderrand. De 5-band onderaan (rij 58) en rechts is weg. Het silhouet van de onderrand is niet aangepast (trapjes op x47, 51, 54, 58 = de modelpunten).
4. **Koepel.** Naden over de hele lengte zichtbaar: boven 6, onder 5/4 (r1: 7 boven, viel weg). Ligging ongewijzigd (gemeten in r1, loopt schuin vanaf de kam en dan omlaag).
5. **Pootjes.** Pootje 2 nu 5×4 rond (rij 59–62), pootje 3 4×3, pootje 4 smaller en rond, 1 en 5 bultjes; 4 en 5 (ver) en 1 in 5, 2 en 3 licht.
6. **Verre oog.** (9,55) en (9,56) van 3/4 naar 5: één pixel gezicht tussen oog en buitenlijn.
7. **Palet.** 4 (146,128,120)→(146,130,112), 5 (182,162,152)→(178,162,140), 6 (206,194,182)→(204,194,174). Rest gelijk aan de larve.

## Ogen (ongewijzigd t.o.v. r1)
A (in de sprite): Weedle `anim_front_gba.png` x16–17, y34–35 op (16–17,55–56); ver oog rechterkolom daarvan op (10,55–56). B: Sewaddle `anim_front.png` x30–33, y32–35 op (15–18,54–57) + ver Weedle 2×2. C: als A, glans in 7 (Snom `front.png` x20–21, y38–39). (16–18,54) is nu 5, zodat de witte glans niet aan de lok vastzit.

## Alphawijzigingen t.o.v. het silhouet (`alpha_wijzigingen.txt`: 22 erbij, 10 eraf)
- Krul 1: +(18,30) lip, +(22,30) +(23,31) +(23,32) rechterlijn (wit in de steel), −(19,31) lucht onder de haak.
- Krul 2: +(26,31) lip, +(29,32) rechterlijn, −(24,32) −(25,32) lobrand één rij lager (holte onder de lip open).
- Krul 3: +(33,34) lip, +(36,35) +(36,36) rechterlijn, −(32,35) −(33,35) holte.
- Krul 4: +(38,37) lip, +(40,37) top, +(41,38) +(41,39) rechterlijn, −(37,38) −(38,38) holte.
- Krul 5: +(42,41) lip, +(44,42) rechterlijn, −(41,42) −(42,42) holte.
- Pootjes: +(40,60) +(41,60) pootje 5; +(21,61) +(25,61) +(22,62) +(23,62) +(24,62) pootje 2 rond; −(34,60) pootje 4 rond.

## Controle (`controle_uitvoer.txt`)
onbenoemde alpha-diff 0 (32 benoemd); open randen 0; losse omlijningspixels 0; losse pixels 0; tintclusters < 3 px 0; selout (3+4) in 10 reeksen van 3–20 px; 8 kleuren + transparant.
Uitgezonderd van de clustertelling: `lijnwerk.txt` (naden, wervelstreepjes, haarlijnen, de schaduwpixels rechts van de loklijnen, witte kern van krul 4 en 5), `pootjes.txt`, oogglans.

## Resterende zwakke punten (eerlijk)
1. **Haakjes van krul 3–5 zijn aangezet**: de holtes (1–2 px) zijn dieper dan in het model (daar ±0,4 px). Zonder die overdrijving lezen ze op 64 px als stekels. Krul 2 is vlakker dan in het model (pet met lipje).
2. **Schaduw is nog geen sikkel** (punt 4 maar half gedaan): de grens wit→beige volgt het model (rij 50 links, aflopend naar rij 53 in de staart) en is nu gebroken door de loklijnen, maar er is geen aparte vormschaduw op de koepel bijgekomen; het model heeft die ook niet.
3. **Loklijnen onderaan** zijn 1-px-diagonalen met een schaduwpixel ernaast; vijf stuks naast elkaar zit dicht bij het zebra-effect. Op 1× lezen ze als veren, op 8× als strepen.
4. **Pootjes 1, 4, 5** blijven bultjes (2 px binnenwerk); rond zijn er 2 (pootje 2 en 3), niet de gevraagde ≥3.
5. **Verre oog** (1×2) is nu los van de rand en op 2× zichtbaar, op 1× nog klein. Variant B (2×2) is daar duidelijker.
6. **Bovenrand kam in 4** is op een lichte achtergrond dun; op donker juist licht. Terug naar 3 is 40 px.
7. De alphalijst is fors (32 px, alleen kam en pootjes); de massa van het lijf is ongemoeid.
