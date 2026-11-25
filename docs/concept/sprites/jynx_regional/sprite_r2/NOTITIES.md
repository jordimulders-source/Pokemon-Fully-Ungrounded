# Regionale Jynx (sirene) frontsprite, ronde 2

Basis: `sprite_r1/jynx_regional_r1.png` + de benoemde reparaties uit `sprite_r1/KEURING.md` (opdracht coördinator, ronde 2). Bouwen: `cd docs/concept/sprites/jynx_regional && python3 sprite_r2/bouw.py`.
Bestanden: `jynx_regional_r2.png` (64×64, mode P, transparency 0, 16 kleuren incl. transparant), `bouw.py`, `vel.png` (r2 8× | r1 8× | model 8× / close-ups 12× naast het model / 1× licht en donker + model 1×).

**Silhouet-diff 0** (assert in `bouw.py`). Gezicht, ogen, mondopening en voetvormen niet aangeraakt, behalve de onderlip (punt 4). (22,10) laten staan (punt 7).

## Afwijkingen t.o.v. r1: 150 px
| zone | px | wat |
|---|---|---|
| klauwen | 9 | klauwgrijs → haar donker (paletplek vrij; iris ongemoeid) |
| haar rechtsboven (x40–44, y11–16) | 15 | één doorlopende strenglijn |
| haarvolume (kruin, voorlok, linkerlok) | 33 | kruinstreng uit het model + lichte haartint |
| linkervleugel bovenrand | 2 | (9,17), (10,17) zwart → veerlijn |
| onderlip (x20–25, y23–25) | 5 | ring naar het model |
| rokvouwlijn (x33–48, y46–48) | 12 | doorlopende 1-px lijn |
| rechterrokpaneel (x35–47, y34–46) | 76 | licht → midden, behalve de bovenrand onder de arm |
(`zones.py` sprite_r1 → sprite_r2: haar 48, vleugels 2, gezicht/lip 5, lijf+rok 86, poten 9.)

## Per punt
1. **Haarvolume.**
   - Palet: plek 15 (klauwen, (100,80,64)) → **lichte haartint (200,154,104)**. De 9 klauwpixels zijn nu haar-donker (84,50,28).
   - **Kruinstreng terug uit het model:** de modellijn natief (53,14)→(57,20) loopt van de kruin naar de lijn tussen voorlok en achterhaar. De reductie hield er alleen het onderste stuk van over, als een S/D-mengsel. Nu één lijn haar-donker (34,7)(34,8)(35,9)(36,10)(36,11)(37,12)(37,13). Rechts ernaast ligt schaduw (35,8)(36,9)(37,10)(37,11)(38,12)(38,13). Dit is geen nieuwe streng: punt voor punt is hij van de modelpixels naar spritecoördinaten gerekend.
   - **Licht (19 px), op de bestaande lokvormen:**
     - Kruin links van de scheiding: boog (24,8)(23,8)(22,8)(21,9)(20,10).
     - Kruin rechts van de scheiding: één boog van de scheiding over de bolling naar de voorlok naast het gezicht. Die is in het midden 2 px dik, (29–31,7–8), en smal aan de uiteinden (26–28,8) en (32,8)(32,9)(33,10)(33,11).
     - Linkerlok waar hij van de kruin over de schouder buigt: (17,15)(17,16)(17,17)(16,18).
   - Overal ligt er middentint tussen licht en buitenlijn, behalve één diagonaal raakpunt bij (22,8). Geen rechte band en geen band langs de buitenlijn.
2. **Haar rechtsboven:** de S/D-afwisseling per pixel is weg. Er is één diagonale lijn op het modelpad van natief (61,19)→(65,26): (41,11)(42,12)(42,13)(43,14)(43,15)(43,16), daarna loopt hij door in de bestaande lijn (43,17–18). Schaduw ligt rechts ernaast, (42,11)(43,12)(43,13)(44,14–16), middentint links. Vanaf rij 17 begint het donkere achterhaar; dat is r1.
3. **Vleugelrand:** (9,17) en (10,17) zijn veerlijn. Zwart en selout wisselen nergens meer om en om (gecontroleerd).
4. **Onderlip:** gebaseerd op de modeldekking.
   - Rij 23: donker x20 en x25, midden x21–24 (één band onder de mondopening).
   - Rij 24: donker x21–24, de onderrand van de ring.
   - (25,23) is nu lijn, waarmee de open rand dicht is. (25,24) blijft wit (model W 7/9).
   - (22,25) donker → wit (model W 6/9).
5. **Rokvouwlijn:** rij 47 is nu één lijn van x33 tot x46, met (47,48) als einde naar de bestaande (48,49). De modelpunten liggen op x34–46 in rij 46–48.
   - De kruisende vouwen zijn op de kruising 1 px: B (40,46) en C (44,46).
   - Dubbele lijnpixels zijn vlak geworden: (39,46) en (38–39,48) midden, (41,46) en (45,46) licht, (46,48) en (48,48) schaduw.
6. **Rechterrokpaneel:** licht blijft alleen langs de bovenrand onder de arm. Dat zijn per kolom x35–39 de bovenste 2 lichte pixels en in x40 de bovenste 1; de rand volgt zo de getrapte armlijn. De rest van het paneel is midden, zoals het model, waar het paneel maar 9 helderheid lichter is.

## Palet (verschil met r1)
Index 15: was klauwen (100,80,64), is nu **haar licht (200,154,104)**. Haar heeft nu 3 tinten + donker: helderheid ±160 / 123 / 89 / 58.

## Controle
- 64×64, P, transparency 0, 16 kleuren incl. transparant, silhouet-diff 0.
- Geen lichte kleur op de buitenrand. Geen selout tussen zwart. Zwart 7,4 %.
- Losse zwarte pixel alleen (25,16), de ooghoek uit het model, zoals in r1.
- S-vlekjes (35,8)…(43,12) zijn de diagonale schaduwlijnen naast de strengen; in 4-buurschap tellen ze als losse stukjes.

## Eigen blik op 8× naast het model, en twijfels
- Het haar heeft nu glans op de bolling en leest rond. Het gezicht, de ogen en de voeten zijn ongewijzigd. De onderlip leest als één ring en de rokvouw als één lijn.
- **Twijfel:** het lichte streepje in de linkerlok (17,15)–(16,18) ligt in de binnenste kolom, tegen de gezichtscontour. De lok is maar 2 px breed: een linkerkolom zou tegen de buitenlijn liggen, en dat is verboden. Wil Jordi het streepje niet, dan zijn het 4 pixels terug naar midden.
- **Twijfel:** het rechterrokpaneel is nu bijna gelijk aan het rokmidden, zoals in het model. Daardoor is de grens tussen paneel en midden alleen nog de vouwlijn.
