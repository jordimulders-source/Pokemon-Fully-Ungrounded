# Kolibrie ronde 2: kleur-frontsprite op het grote silhouet (24 okt)

Bestanden: `kolibrie.png` (64×64, geïndexeerd, 16 kleuren, index 0 transparant), `vel.png` (ronde 1 en 2 op 3× en 1×, silhouet v6 groot op 3×, ronde 2 op 1× op vier achtergronden, 1× naast Venomoth, Ho-Oh, Fearow, Articuno, Talonflame en Ninjask), `teken.py` (met de hand getypt tekst-raster; het script zet alleen die pixels), `check.py` (pixeldiff), `vel.py`.

## Wat er t.o.v. ronde 1 veranderde (punt voor punt uit de keuring)
1. **Groter:** opnieuw getekend op `silhouet_v6_groot_1x.png` (986 px); sprite nu 1035 px (ronde 1: 783). Kop, oog (2×3: bovenlid, glanspixel, lichtere reflectie), doorschijnende vleugelpunten en "geen schubben" meegenomen.
2. **Vleugel en lijf apart:** lijf nu diep verzadigd violet (`V` 142 54 214, schaduw `w`, hooglicht `L`, omlijningsbasis `v`). Vleugels beginnen in donker fluweel (`k`/`h`, hooglicht `H` langs de voorrand, `K` aan de achterrand), dan lila-grijs `m` met fluwelen pennenlijnen, dan bleek `p`, punt `P` met lichte rand `m`: drie stappen, zoals Venomoth. De verre vleugelwortel is donkerder (`k`) dan de nabije, zodat de voorrand van de nabije vleugel ervoor leest. Op 1× (vel) lezen vleugel en lijf als twee delen.
3. **Slierten:** nu 3 px breed: donkere binnenrand `K`, glanzende middenlijn `V`, lichtere buitenrand `v` (licht van linksboven). Racketpunten als zielevlammetjes met omlijning (`m` aan de lichtkant, `w` aan de schaduwkant), bleke vulling `p`/`P` en één kernpixel `W`: A (rechts, 4×4), B (midden, nu 4 rijen hoog, was een streepje), C (links onder, 5×5). Alle drie zichtbaar op 1×, ook op wit en donker.
4. **Blauwgroen:** één vlak op de schouder tussen kop en vleugelwortel (rijen 23–29), drie tinten (`t` rand/schaduw, `T` basis, `U` hooglicht linksboven), afgerond boven en onder. Op 1× duidelijk zichtbaar.
5. **Kuif:** drie veertjes in violet (lichtkant `V`, schaduwkant `v`) met bleke punten (`P`/`p`, 2–3 px per veer), losstaand met 1 kolom lucht ertussen; het eerste veertje leunt bovenaan 1 px naar achteren. Geen zwarte stekels meer (die lazen als geweitje).

## Pixeldiff t.o.v. silhouet_v6_groot_1x.png
1035 px (silhouet 986): **56 erbij, 7 eraf**, alles op ≤ 1 px van de omtrek:
- Slierten 3 px breed (opdracht punt 3): 41 px aan de binnenkant van de drie slierten (o.a. (49–53,36), (54–56,37), (57–58,38), (59–60,39–46), (42–45,41–52), (52–56,44–52)).
- Racketpunt B groter: (48–50,52) en (47–49,55) erbij; (46,53), (45,54–56) eraf (lucht tussen sliert 3 en racket B).
- Kuif: (12,12), (12,13) eraf, (14,12), (14,13) erbij: eerste veertje leunt naar achteren.
- Voorhoofd: (4,26), (4,27) erbij: rechte voorkant van 6 px wordt een curve.
- Buik: gat (29–31,39) dicht.
- Staartfranje: (47,41) eraf (los puntje); (58,49), (58,50), (57,51) racket A afgerond.

## §0-checklist (SPRITING.md)
1. 3/4 naar links-voor: ok (silhouet; verre vleugel smal, hoger en donkerder).
2. Alles geteld en verbonden: snavel, kop met één oog, kuif (3), 2 vleugels, schouder, lijf, franje, 3 slierten met elk een vlammetje. Ok.
3. Geen rechte lijnen waar hij rond is: voorhoofd en buik afgerond; blauwgroen vlak afgerond.
4. Oog geïntegreerd: ok, klein (Jordi: "het oog mag veel kleiner").
5. Silhouet leest als kolibrie: ok.
6. Formaat: 1035 px, box 62×60; naast Fearow/Articuno nu vergelijkbaar in breedte, nog wel slanker (hoort bij een kolibrie).
7. Pose niet stijf: ok (drinkende zweefpose).

## Harde eisen SPRITE_NORM
1. Leest op 1× als Pokémon: ok (vel, onderste rij).
2. 3/4 links-voor, kop meer naar de kijker: ok.
3. Delen vast aan het lijf, geen gat vleugel–lijf: ok.
4. Geen Escher: nabije vleugel over de verre; sliert 2 loopt tussen sliert 3 en racket A door, racket B ligt boven sliert 3; overal gescheiden door donker/bleek of 1 px lucht.
5. Silhouet bevroren (uit Jordi's foto); geen doosvormen.
6. Kop: plat bovenhoofd, niet rond.
7. Ogen: ok.
8. Kenmerken op 1×: snavel, kuifpunten, schouder, vleugelpunten, 3 vlammetjes: ok. Schubben bewust niet (las in ronde 1 als ruis).
9. Omlijning per kleurgroep, zwart alleen aan de schaduwkant: zie hieronder.
10. Geen Chernobyl: ok.

## Dragonfly Cave-regels (SPRITING §1–§8)
- §1 Geen vormgereedschap: alles getypt in `teken.py`.
- §2 Per onderdeel: kop/oog → schouder → vleugels → lijf → franje → slierten → vlammetjes → kuif; elk onderdeel op 8× bekeken en bijgewerkt.
- §3 Curven: voorhoofd 1-1-2-2-2-2; slierten als regelmatige trappen zonder knikken; pennenlijnen als 2-1-2-trap langs de vleugelas.
- §4 Palet: per groep basis/schaduw/hooglicht + omlijningstint (fluweel k/h/H + K, violet w/V/L + v, blauwgroen t/T/U), vleugel m/p/P, kern W. 16 kleuren, geen extra verlopen.
- §5 Licht linksboven: hooglicht op kruin, voorhoofd, schouder (U), nek/flank (L), voorrand vleugelwortel (H); schaduw op keel, buik en achterrand van de vleugelwortel; slagschaduw `w` op het lijf onder de vleugel.
- §6 Glans: één glanspixel in het oog, één kernpixel per vlammetje; verder geen glimpjes.
- §7 Texturen: veren glad; geen schubben.
- §8 Omlijning: kop `k` boven/voor, `K` onder; lijf `v` op de rug, `K` aan de buik; vleugels `k`/`h` voorrand, `K` achterrand bij de wortel, `m` aan de punt; slierten `K` binnen, `v` buiten; vlammetjes `m`/`w`. Altijd 1 px, geen antialiasing aan de buitenkant.
- Making Fake Pokémon: drie hoofdkleuren (fluweel, violet, blauwgroen) + bleek Ghost-licht; geen detail dat niet op 1× leest.

## Wat nog niet klopt (eerlijk)
- Op een heel donkere achtergrond (vel, vakje linksonder) verdwijnen kop en vleugelwortels: dat hoort bij "fluweelzwart" en donkere vleugelwortels (zelfde als Murkrow/Honchkrow). Op lichte en middentoon-achtergronden leest hij goed. Geen reparatie zonder het gevraagde fluweel los te laten.
- De slierten zijn nu 56 px buiten het silhouet verbreed (±1 px, op verzoek). Als Jordi de slanke slierten van v6 wil houden, is dat terug te draaien door de binnenrand weg te laten.
- Verder vind ik geen zwakke punten. Wat ik onderweg zwak vond, heb ik gerepareerd: zwarte kuifstekels (lazen als geweitje → violette veertjes met bleke punten), blauwgroen als rechthoek (afgerond), losse pennenstipjes (doorlopende lijnen), racket B als streepje (4 rijen hoog), rommelige franje met zwarte strepen (glad violet), verre vleugelwortel die met de nabije versmolt (donkerder).

## Lessen
- Een donkere vleugelwortel tegen een donkere kop leest alleen als de verre wortel nog een stap donkerder is en de nabije voorrand een hooglicht (`H`) heeft.
- Een dunne sliert krijgt aanwezigheid door 3 px: donkere rand, glanzende middenlijn, lichtere rand; 2 px met alleen omlijning leest als spinnenpoot.
- Een vlammetje heeft minstens één binnenrij nodig (rand–vulling–rand) om op 1× als vorm te lezen; anders wordt het een streepje.
- Kleine kuifveren in zwart lezen als stekels/gewei; in de lijfkleur met bleke punten lezen ze als veren.
- Pennenlijnen als doorlopende 2-1-2-trap tekenen; losse pixels lezen als stippels.
