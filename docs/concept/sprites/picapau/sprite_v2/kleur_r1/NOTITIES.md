# Picapau sprite_v2 kleur r1: notities (maker, 5 nov)

Bestanden: `teken.py` (de rijen met de hand als (x, tekens), r5-details letterlijk overgenomen) → `raster.txt`; `bouw.py` → `picapau.png` + `normal.pal`; `controle.py` → `controle_uitvoer.txt`; `vel.py` → `vel.png` (8x: render | sprite | Taillow | Pikachu; onder 1x en 2x); `zoom.py` (hulp: uitsnede render naast sprite).

## Overgenomen uit kleur_r5 (Jordi: "details bewaard blijven")
- **Palet** r5 (zelfde tekens/volgorde); alleen `l` bijgesteld van 168,114,62 naar 200,130,72 (licht roodbruin), zodat de staart een eigen licht heeft en de vleugelschouder warmer is.
- **Kuiftoppen** rijen 3–8: 0 px verschil (script).
- **Pikachu-oog** x25–28, r18–21: 0 px verschil.
- **Wang** (c/C, r23–26): 0 px verschil in de wangpixels (2 px in de zone zijn geel om de wang heen).
- **Vleugelschubben** (twee rijen, r27–28 en r31–33): 0 px verschil; ook de bovenvleugel r24–33 grotendeels r5.
- Kuifbasis r9–11 en de kopbovenrand r12–16 (lijnen en kooplicht) uit r5; alleen de schaduwsikkel rechts is nieuw.

## Nieuw, naar de render (B1)
- **Snavel**: kegel schuin omhoog naar links (punt x15 r17, basis x19–20 r18–23, 3–4 px dik), bovenkant licht hoorn, onderkant `g`, basis donkergrijs `G` zoals de donkere snavelbasis in de render; zwart alleen langs de onderrand.
- **Verre oog** piept boven de snavelbasis (x19–20 r17), zoals in de render: geeft de 3/4.
- **Kopvolume**: schaduwsikkel rechts, smal boven (2 px) en breder naar onder (6–8 px), die onder de wang doorloopt; tapse binnenlijn `4` kop-over-borst alleen aan de schaduwkant (x30–33 r27–28).
- **Achterste kuifpunten** (r12–13, r17–19) met een punt van 1 px verder, bovenrand goudbruin i.p.v. zwart.
- **Vleugel**: bovenvleugel blijft, onderrand met ronde elleboog (r35–36) en daaronder de slagpennen als smalle diagonale band tot over de staartbasis (render), lijf zichtbaar eronder in slagschaduw.
- **Lijf**: borst- en buik/dijbolling elk een eigen hooglicht linksboven, schaduw rechts onder de vleugel en langs de buikonderkant; buikonderrand als boog (r45→r46→r47→r46) i.p.v. een rechte lijn; kort tap binnenlijntje bij de dij.
- **Staart**: bol (r46–50, licht `l` linksboven, `b` rechts) met insnoering r51, dan dunne stijve punt tot r57.
- **Poten**: nabije poot grijs, lange teen naar links met haakklauw (x24–25 r47–48) en korte teen naar voren; verre poot rechts erachter in `G`, met teen en klauw (x37–38).

## Controle (controle_uitvoer.txt)
- Lichte kleur op de buitenrand 0, losse pixels 0. Tintclusters < 3 px in vulkleuren: alleen de r5-schubben (textuur, bewust), snavelpunt (2 px `g`, 1 px `h`) en (33,9) uit de r5-kuif; de rest zijn lijnpixels (selout/binnenlijn).
- **Buiten het silhouet: 30 px**: kuiftoppen r4–6 (6 px, al zo in r5, label K), snavelpunt (16,17) en (18,18) (label N), kuifpunten (40,12) (41,18) (40,19), buikboog (39–41,47) (render-label Y), poten/tenen/klauwen r45–49 (16 px, label P of klauw). Leeg gelaten: (32,46) (lucht tussen de poten).
- 847 px, 15 kleuren + transparant.

## Jordi's zes punten (eerlijk)
1. **"volledig 2d"**: beter dan r5 (kop als bol met sikkel, vleugel over het lijf met slagschaduw, gebogen buik), maar **niet ok**: de grote lichtvlekken op borst en buik lezen nog als losse vlakken en het lijf mist de zachte schaduwrand rondom die de render rond maakt.
2. **"geen drie kwart"**: ok-ish: één oog, snavel aan de linkerrand, verre oog piept, verre poot achter. Het lijf zelf is het bevroren silhouet.
3. **"perspectief klopt niet"**: ok-ish: verre poot rechts en donker, vleugel ligt over het lijf, staart erachter.
4. **"klauwen afgeknapt"**: half: tenen steken nu uit met haakklauwen; op 1x lezen ze als kleine grijze voetjes, de klauwen zelf net.
5. **"shading niet goed"**: half: licht linksboven en sikkels kloppen, maar zie punt 1 (vlekkerig hooglicht).
6. **"snavel is weg"**: beter: op 8x een duidelijke kegel met donkere basis; op 1x een klein licht puntje schuin omhoog. Kleiner/minder massief dan in de render (de render-snavel is op 1x maar 3–4 px dik).

## Zwakke punten (dus niet klaar voor Jordi)
- Hooglichtvlekken borst/buik: "stickers"; liever één doorlopende lichtzone met een zachtere overgang (bv. kartelrand of één extra tussentint) en de schaduwrand langs de onderkant breder.
- Snavel op 1x klein; eventueel 1 px langer/dikker (buiten het silhouet, label N).
- Achterste kuifpunten zijn 2 px dik; lezen op 1x als kleine stekels, minder als de kegels van de render.
- Voetjes druk op 8x (veel zwart onder de tenen).

## Lessen
- Een aanpassing van een gedeelde helper (regex op S-rijen) faalde stil voor rijen met een commentaar erachter: controleer of elke wijziging echt landde (assert per rij).
- Uitsnede render | sprite op 10–14x per onderdeel (`zoom.py`) liet direct zien wat er mis was (snavelvorm, zwarte voetbalk), sneller dan het hele vel.
- Kopvolume: een verticale schaduwband leest plat; de sikkel moet boven smal en onder breed, en onder de wang doorlopen.
