# Poedelmot: kleur r6 (maker, zuinig)

**Maatstaf (Jordi, letterlijk):** "de keurder moet alleen kijken naar de accuraatheid tov het oorspronkelijke model, verder verander je NIKS, dat model is perfect en moet zo accuraat mogelijk vertaald worden". Daarom is na de eerste r6-opzet teruggedraaid wat niet in het model staat:
- De drie gebogen **aders** (Venomoth-stijl van de keurder) zijn weg; die staan niet in het model.
- De **kinboog** is weer de dunne donkere boog onder het snuitvlak, zoals in het model, met de dip bij x22–25 en links doorgetrokken tot (19,41).
- De **sprietribben** lopen weer schuin "\" op beide sprieten, zoals in het model, in één tint per rib.
Wat in het model staat, is gebleven: geschulpte zoom en onderrand, kuifplukjes, scheidingslijn bij de linkervleugel en ronde pluimtoppen.

Gebouwd vanaf r5 (r5 ongewijzigd) na `kleur_r5/poedelmot.png.keuring.md`. Jordi: vormen en belijning boven kleur.

Bestanden: `raster.txt`, `poedelmot.png`, `normal.pal`, `palet.py`, `vel.py`/`vel.png` (r6 | r5 | bron 8× en close-ups), `controle.py` met `controle_uitvoer.txt`, `stappen/bouw6.sh`. Nieuwe lagen: `k_r6.py`, aangepaste `k_vleugel5.py` en `k_spriet5.py`.

## Gedaan
1. **Vleugelnaden**:
   - De zoom tussen voor- en achtervleugel en de onderrand van de achtervleugel zijn diepere geschulpte bogen met ongelijke lobjes (amplitude 2–2,4 px). Rij 36 en rij 45/46 zijn dus geen rechte lijnen meer.
   - De voetlijn bij de kop is één zachte lijntint (`4`, taps in `6`) in plaats van een donkere kolom.
   - (De aders uit de eerste opzet zijn weer weg: niet in het model.)
2. **Mond/kin**: dunne donkere boog zoals het model (zie boven). Kruin: de buitenrand (22–25,27) blijft selout `4` (Gen 3: geen lichte kleur op de buitenrand); de witte plukjes van het model staan direct eronder.
3. **Linkervleugel**: een tapse binnenlijn (`7`→`3`→`7`) van (12,28) tot (14,37) scheidt de lob achter de kop van het gezicht.
4. **Pluimen**: ronde bovenbogen op pluim A en B. De klauwtjes zijn de gerichte stompjes uit r5. (21,55) ligt buiten het silhouet en blijft zo.
5. **Sprietbaarden**: doorlopende ribben in één tint (`4`), om de 3 px, schuin zoals het model. De om-en-om-1/3-kammetjes zijn weg.

## Controle
- **Alpha-diff 0**. Open randen 0 (uitzonderingen: klauwtjes, sprietpunt).
- Selout zonder afwisseling. Losse pixels 0, clusters < 3 px 0.
- Donker-aandeel 0,229.

## Maatstaven (Jordi): gelijkenis met het model en Gen 3-eisen
Gelijkenis: niets toegevoegd of weggelaten t.o.v. het model (aders teruggedraaid). Gen 3: controle schoon (zie boven). Open punten staan hieronder.

## Eerlijke zwakke punten
- De tan schubkrullen op de vleugels zijn nog grover en kleiner dan in het model.
- De sprietribben om de 3 px lezen op 8× nog licht als raster.
- De pluimen zijn alleen aan de bovenkant ronder; de onderkant volgt het silhouet.
- De voetlijn op x37–41 loopt nog steeds vrijwel verticaal. Het silhouet en de vleugelvoet laten daar weinig ruimte.
- Eindstand één keer op 8× naast het model bekeken; geen close-ups per onderdeel meer nagelopen (gebruikslimiet).
