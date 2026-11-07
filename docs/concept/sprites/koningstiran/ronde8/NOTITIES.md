# Sapa Inca – ronde 8 (stafkop: zon uit de veer, groter)

Basis: `ronde7b/sapa_inca.png` (ronde 7 met de linkeromtrek van de coördinator op rij 49–53), in `sapa_inca.txt` als volledig raster met de wijziging onderaan in het blok "ronde 8". Bestanden: `sapa_inca.png/.txt`, `bouw.py`, `controle8.py`, `vel.py` → `vel.png` (stafkop 10× naast variant B van ronde 7; 4× licht/donker; 1× naast variant B en ronde 7b), `kijk.py`.

Jordi: "stafkop zon uit veer is prima, maar mag wat groter".

## Wat er veranderde
- Variant B is als vertrekpunt genomen en de zonneschijf vergroot van 5×4 naar **7×7** (goud x12–18, rij 21–27): een ronde schijf (breedte per rij 3, 5, 7, 7, 7, 5, 3) met de lichte tint (y) linksboven, g als basis en een a-rand. Hij groeit uit de veerpunt: de roestbruine vaan (t) loopt om de onderkant van de schijf (rij 26–27) en gaat over in de schacht (rij 28–29, verder ongewijzigd).
- Waar de zon vóór de kroonrand en het kroonkwastje ligt, staat een zwarte omlijning (K): boven op rij 20, schuin langs rij 21–22 en links langs het kwastje op x11 (rij 23–27). Aan de lichte kant (rechts, tegen transparant) is de a-rand zelf de omlijning.
- Symmetrisch rond de schacht x15, geen losse stralen of pixels.

## Controles (`controle8.py`)
- **Diff t.o.v. 7b:** 50 px, allemaal in de stafkopzone x11–19, rij 20–29; **erbuiten 0 px** (gezicht, kroon buiten de zon, lijf, buik, poten, vleugels, de rest van de staf).
- **Bedekte kroonpixels:** **21** (kroonrand rij 20–22: 13 px; kwastje x11–14, rij 23–25: 8 px). Het kwastje blijft zichtbaar als smalle hangende veer (x10, met de K-rand van de zon ernaast) en loopt onder de zon door naar zijn lavendel-zwarte punt.
- **Silhouet:** +17 px (1622 → 1639).
- 0 open randen.

## Zelf gekeken (10×, 4×, 1× naast variant B van ronde 7)
- Op 1× leest de kop nu als een duidelijke gouden bol/zonneschijf bovenop de staf (scepter), duidelijker dan de kleine knop van variant B.

## Eerlijk: wat nog niet klopt
- **Het is meer een gouden bol dan een zon:** er zitten geen stralen of veerpunten rondom (dat zou op deze maat snel ruis worden). Alleen de vaan onderaan laat zien dat hij uit de veer groeit.
- **Het kroonkwastje links is grotendeels bedekt:** het is nu een smalle streep (1 px kleur + 1 px K) naast de zon. Het kwastje kan op 1× wegvallen tegen de staf.
- **De zon raakt de kroonrand:** het donkere randje tussen zon en kroon maakt op 4× de onderkant van de kroon daar wat zwaarder.

## Lessen
- Een stafkop die vóór de kroon ligt, krijgt een K-rand alleen waar hij een ander deel overlapt; aan de transparante kant is de eigen a-rand genoeg (minder zwart, rondere vorm).
