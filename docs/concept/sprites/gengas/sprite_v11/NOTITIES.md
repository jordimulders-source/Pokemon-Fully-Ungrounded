# Gengas sprite v11 (15 nov) = v10a + gezicht 125% + geen vlek meer
Keten: `python3 v11.py && python3 maak.py && python3 vel.py`. 481 pixels, reden per pixel in `raster.txt.log`. **Diff buiten x 4–48, y 22–48 = 0** (gemeten).
1. **Geen vlek, geen spiraal.** Jordi: "de stormvlek is niet mooi zo, als die niet goed immersed toont, heb ik liever dat je het reguliere golfpatroon aanhoudt, die is erg mooi gelukt". De lichte strook (l) links van de plek loopt door met een schuine rechterrand (laatste l-kolom per rij 30–41: 35,35,35,36,36,37,37,38,38,39,39,37). Rechts daarvan ligt de middenband m, zoals ernaast.
2. **Gezicht 125%** uit `gezicht_groter/gezicht_1.25.npy`, geplaatst op (i+6, j+27). Dat is hetzelfde middelpunt als het oude blok (Gengar x−6, y+5).
   - Kleuren: e→a, f→K, 1/5/6 Gengars waarden, 3 = slot u, 2/7 = H. Gengars d wordt niet geplakt (bandtint).
   - Nagelopen tegen Gengar (17 pixels, FIX in v11.py): tandscheidingen 1 px en verspringend zoals Gengar (boven x21/24/29/33, onder x25/30/34 in Gengar-termen), tandschaduw 7-2 van 1 px, rechtermondhoek K 1 px breed met diagonale trap, linkerpupil 2-2-1 gespiegeld aan de rechter (beide pupillen tegen de binnenste wenkbrauwlijn).
   - Gengar heeft geen lichtroze glans in de ogen (idx 4 komt in zijn gezicht niet voor), dus die is er ook niet.
   - Het oude gezicht is weg; de gaten zijn gevuld met de buurtint.
   - Voorhoofdband opnieuw: onderrand 1 rij boven de grotere ogen, golvend (volgt de wenkbrauwen, zakt tussen de ogen tot rij 32), daaronder m.
Zwakke punten (eigen): de bovenkant van de linkerpupil grenst aan lijftint m (bij Gengar is dat d, hier bandtint volgens de afspraak); de band boven het rechteroog is dun (onderrand rij 27–28) en heeft een m-inkeping op rij 28 x30–32; de lichte strook naast de rechtermondhoek is smal en verticaal (x31–35).
