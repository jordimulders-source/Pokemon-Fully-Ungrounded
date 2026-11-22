# Overworldsprite viscacha, eigen methode zonder Gemini (19 nov)

Bronnen (bevroren): front `viscacha/af/viscacha.png` + `normal.pal`, rug `viscacha/rug/af/rug.png`, icoon `viscacha/icoon/af/icon.png`.
Regels: OW-meetstudie `rug_icoon_studie/overworld/meting_onderdelen/RESULTAAT.md`. Scripts: `../scripts/`, bronrasters: `../bron/`, rondes: `../werk/`.
Alles draaien vanuit de repo-root.

## Stappen die echt gedaan zijn
1. **Onmisbare kenmerken** (uit de icoonlessen): lange ronde oren dicht bij elkaar, slaperig oog (donker met glans en zwaar, hangend bovenlid), gele bliksemwangpluk, staart met gekartelde gele pluim; daarnaast snorharen en crème borst.
2. **Palet** = de frontkleuren zelf (`ow_pal.py`), plus omlijning: 1 = donkerbruin (80,44,24) voor bovenranden, 2 = zwart voor onder/opzij. 15 kleuren. Hoofdvlakken dus even licht en verzadigd als de front.
3. **Opzij (frame 4)** — eerst het icoon als onderlaag geprobeerd (`stap1_icoon_onderlaag.py`, `stap2_schuif.py`); verlaten na de meetstudie: OW-opzij is bij 15/15 een echt profiel met een vaste kop van ±9×9, het icoon is driekwart. Daarna:
   - `stap3_onderdelen_opzij.py`: de front in onderdelen (de polygonen van het icoon, `icoon/onderdelen/delen.py`) per groep verkleind met vaste factoren uit de studie (lijf 0,45×0,39, kop 0,43×0,60 rond de hals, oren 0,40; opgeheven poot eruit). Geeft houding, bolle rug, S-staart en pluim; ruw, alleen als gids.
   - Met de hand als tekstraster (`bron/opzij.blk`, 4 blokken van 8 kolommen, `blk.py` controleert de lengte): kop 10×9 profiel met snuit naar links, oog op 0,45 van de snuit en lager in de kop, oren 4–5 px boven de kop (verre oor links erachter zoals in de front), wangpluk achter het oog met gouden punt over de nekrand, bult achteraan de rug, staart uit de heup naar rechts en omhoog met de pluim van het icoon, 2 poten van 2–3 px, crème borst, snorhaarstompjes buiten het silhouet.
4. **Voor (frame 0)** — linkerhelft als raster (`bron/voor.half`), `spiegel.py` maakt hem symmetrisch (kolom 15 = midden; rechts buitenste kolommen naar schaduwtint 5). Kop 15 breed × 10 hoog, breder dan de oren (oren bovenop, niet in het verlengde van de kopzijkant: anders leest het als kat), ogen 5 px uit elkaar, oog = bovenlid + één donkere rij met glans en een hangend ooghoekje (= slaperig, zoals de front), neus, wangpluk die buiten de wang uitsteekt in goud, snorharen, crème borst, twee voorpoten. Staart weggelaten (6/15 echte OW doen dat): tussen de oren las de pluim als kroontje.
5. **Achter (frame 2)** — ook gespiegelde helft (`bron/achter.half`): achterkant van de oren bruin (zoals de rug), kop 15×6 boven, smallere hals, bredere heupen (peer), staart midden over de rug omhoog met de pluim op de rug/nek (niet boven de kop), voeten 2 px.
6. **Loopframes** in `bouw_ow.py` als kleine wijzigingen op het stilframe: voor/achter één voet 1 px op + oor 1 px omlaag; opzij voorpoot 1 px naar achteren. 12–13 px verschil, figuur blijft staan.
7. **Bouwen en meten**: `bouw_ow.py` (overworld.png, .pal, 8×, loop.gif), `meet.py` (maat, onderkant, midden, symmetrie, kleuren, randhelderheid, eenlingen, loopframes), `vel.py` (vel_vergelijk.png met rattata/eevee/sentret), `toon.py` (snelle 8×-proef van rasters naast de front).

## Lessen voor de volgende soort
- Begin direct met de meetregels (vaste kopmaat), niet met het icoon als onderlaag als de front/het icoon driekwart is.
- De onderdelen-verkleining is een goede gids voor houding en massa, niet als pixellaag (ruis); tekenen op een tekstraster met vaste blokken van 8 kolommen voorkomt verschoven kolommen.
- Symmetrische aanzichten: alleen de linkerhelft tekenen en spiegelen.
- Kop breder dan de oorbasis, anders een kat; half dicht oog (lid + 1 rij) leest als slaperig.
- Gele details niet laten samenvloeien (wangpluk + pluim werd in de achterkant één gele band: wangpluk daar weggelaten).

## Ronde 2 (na de coördinator: "rechtopstaande kat, blokkig")
Ronde-1-bronnen staan in `../werk/ronde1_bron/`. `bouw_ow.py` centreert nu elk aanzicht zelf (midden x15-16, onderkant y29) en `spiegel.py` kent `Z y x pixels` voor asymmetrische delen (de staart) na het spiegelen.
1. **Oren** overal ronde schelpen: 2 px dop, 4–5 px breed, donkere binnenkant (d), 4–5 rijen boven de kop, dicht bij elkaar. Van achteren: bruine achterkant.
2. **Voor gehurkt**: kop 13 breed met bolle wangen, daaronder bolle heupen links en rechts (tot 17 breed), korte voorpootstompjes (3 px) en hielen, kleine crème borst zonder harde kinlijn (anders leek het een open mond). Staartpluim rechts achter de kop (de staart krult in de front achter het lijf omhoog), steel verdwijnt achter de wang.
3. **Achter**: peervorm met ronde achterkop en bolle heupen. De staart loopt vanuit de stuit schuin over de linkerheup (bruine band met een donkere lijn eronder), buiten het lijf verder omhoog, met de gekartelde pluim naast de kop. Geen geel vlak meer onder de nek.
4. **Opzij**: rug als één boog van nek tot stuit, kruin en snuit ronder en spitser (voorhoofd loopt schuin af), achterpoot gehurkt met bolle dij (binnenlijn) en lange voet naar voren, staart in S: uit de heup naar rechts, omhoog, pluim bovenaan terug naar links.
5. **Binnenlijnen**: dij over lijf, kop over lijf (achterkant), staart over heup, ooglid, mond. 27–29 lijnpixels per stilframe.
Les: een uitlijnfout of te korte oren zie je pas op 8× via `toon.py` met een nieuwe bestandsnaam (de viewer toonde een oude versie van een overschreven png).
