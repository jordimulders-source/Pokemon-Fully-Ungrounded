# Picapau-evolutie: sprite r7 (drie zones op r6, rest bevroren)

r6 (`../r6/`) blijft staan. Geen modelwerk.

## Jordi letterlijk (over r6)
**"ik wil beide krullen bovenop naar achteren en die snavel is geen snavel, kijk bijv naar fearow of andere vogels, echt lelijk. Voor de rest is die wel prima. Alleen de buik is niet meer mooi ovaal. De pose is prima"**

## Bevroren: bewijs
- `diff.py` → `diff_uitvoer.txt`: **0 px verschil buiten de zones**, in `raster.txt` én in `picapau_evo.png`.
- De zones zijn rechthoeken: snavel x6-22 y7-14, krullen x14-46 y0-8 en buik x9-28 y15-35.
- Per zone staat erin welke pixels veranderden (oud>nieuw).
- Binnen de zones is alleen het eigen onderdeel aangepast. Twee bijwerkingen:
  - Onder de nieuwe snavel verdwijnt een stukje van de verre vleugel (rij 9-14). Waar de oude snavel lag, is de vleugel weer dicht gemaakt.
  - Waar de verre krul eerst zat, links van de kop (rij 0-4), is het nu leeg. De vleugelrand blijft daar staan zoals hij was.

## 1. Snavel: studie van echte Gen 3-sprites (`ref_snavels.png`, 8×)
- **Fearow**: lang, dun (3-4 px breed), licht gebogen, met een scherpe punt van 1-2 px.
  - Omlijning aan de lichtkant (links) in donkerrood (j), niet zwart. Daarbinnen een smalle lichte strook (g, lichtroze) langs de hele bovenrand, dan de basistint (h).
  - Zwart (k) alleen aan de schaduwkant/binnenkant.
  - Licht open: twee punten met een smalle spleet ertussen. De ondersnavel is duidelijk korter dan de bovensnavel.
  - Hij zit vast als één vorm uit de kop, zonder rand op de naad.
- **Pidgeot**: kort en haakvormig.
  - Twee tinten roze (licht boven, donker onder), zwarte omlijning en een zwarte mondlijn, met een witte glansstip.
  - De punt buigt omlaag.
- **Staraptor**: kort, oranje, met een haak.
  - Licht (n) boven, schaduw (o) onder, een donkerbruine mondlijn (m, gekleurd!) en een zwarte onderrand.
  - De bovenrand is één boog.
- **Spearow**: kleine roze haaksnavel, licht bovenop, een donkere onderrand en een korte mondlijn.
- **Skarmory**: open bek.
  - Een lichte, staalblauwe bovenplaat met een donkere blauwe rand.
  - De mond is binnen donker/rood, met een duidelijk kortere onderkaak.
- **Picapau (pre-evo)**: korte grijze wig.
  - Donkergrijze omlijning (d), een lichte hoornstrook (f), grijs midden (e) en zwart op de naad onderaan.
- **Wat ze delen:**
  - één vorm met een gebogen bovenrand en een scherpe punt;
  - lichte strook langs de bovenrand, schaduw onder;
  - zwart alleen aan de schaduwkant of als mondlijn, met een gekleurde lijn aan de lichtkant;
  - een kortere onderkaak.
  - Nergens horizontale balken of strepen over de hele snavel.

## Snavel r7 (`tekening.txt`, onderaan)
- Een lange beitelsnavel (15 px, van de kop tot x7), licht open, schuin naar links-onder.
- **Bovenrand** (G, donkergrijs als gekleurde selout zoals Picapau):
  - een boog met trappen van 3-4-3-2-2-1 px per rij, dus steeds steiler naar de punt;
  - de punt eindigt in 1 px.
- **Licht**: een strook van 1 px crème (a) direct onder de bovenrand (zoals de g-strook van Fearow), daaronder grijs (g).
- **Mondspleet**: een dunne zwarte lijn (k) die van de mondhoek tot in de punt loopt. De mondhoek is 3 px rood (C).
- **Ondersnavel**: 4 px korter (punt x11 tegen x7), lichtgrijs boven en schaduw G onder.
- Palet ongewijzigd (zelfde als r6). Grijs-hoorn zoals Picapau gekozen: een lichte hoornkleur viel weg tegen de crème keel eronder.

## 2. Krullen
- Het **nabije oor** wees al naar achteren (spiraal rechts van de kop) en is ongewijzigd.
- Het **verre oor**:
  - begint nu linksboven op de kop, met een wortel van 2 px (kGGGk) zoals het nabije oor;
  - loopt over de kruin (rij 0) naar achteren en zakt één rij;
  - eindigt in dezelfde 1px-spiraal met gat als het nabije oor, één stap hoger en verder naar achteren (x40-45, rij 1-7).
- Zoals bij Raichu Gen 1 liggen de twee oren boven elkaar en wijzen ze allebei naar rechts.

## 3. Buik
- Rij 18-30 en 35 opnieuw.
- **Links**: een gladde boog (x 15-13-12-11-11-10 ×7-11-11-12-13-14). Daardoor verdwijnt de lange rechte diagonaal van r6 en de bult linksonder.
- **Rechts**: 27 ×7, 26 ×3, 25-25-24-24-23-22-21-19. Het rechte stuk in r6 was 9 rijen lang.
- **Onderkant** rond: rij 35 is crème van x16 tot 19, met één oranje pixel ervoor.
- **Licht** (a) als ovaal linksboven, **sikkel** e rechtsonder (2 px breed bovenaan, 4 px onderaan).
- De keel (rij 15-17) is ongewijzigd, omdat de verre vleugel daar ligt.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen tintclusters kleiner dan 3 px.
- 15 kleuren + transparant, 1769 px.
- Alleen-diagonaal verbonden: 2 px (de spiraallijnen).
- De 4 g-pixels op de rand zijn de nabije voet; die is ongewijzigd uit r6.

## Bestanden
- `picapau_evo.png`, `normal.pal`, `raster.txt` en `tekening.txt`.
- `controle_uitvoer.txt` en `diff_uitvoer.txt` (`diff.py`).
- `vel.png` (`vel.py`): 1× en 8×, r7 naast r6, Fearow, Pidgeot, Picapau en Raichu Gen 1.
- `kop_closeup.png` (`kop_closeup.py`): de kop van r7 en r6 op 16× naast de snavels van Fearow, Pidgeot, Staraptor en Picapau op 16×.
- `ref_snavels.png` (`ref_snavels.py`).
- Uit r6 meegekopieerd en niet gebruikt in r7: `schuin.py`, `draai_proef.py`, `tekening_basis.txt` en `vel_leunen*`.
- Draaien: `python3.11 zet.py && python3.11 bouw.py && python3.11 controle.py && python3.11 diff.py && python3.11 vel.py && python3.11 kop_closeup.py && python3.11 ref_snavels.py`

## Eerlijke zwakke punten
1. **Hoek van de snavel.**
   - Hij loopt vrij vlak (±23°). Fearow wijst veel steiler omlaag.
   - Voor een specht is de vlakkere hoek kloppend, en hij leest op 1× als een lange snavel.
   - Wil Jordi hem schuiner, dan kan de punt 2 rijen lager (rij 15). Dan dekt hij meer van de verre vleugel.
2. **Strepen in de snavel.** Er zitten 6 tintstroken boven elkaar (G-a-g-k-g-G). Op 8× is dat een beetje streperig. Fearow doet hetzelfde, maar met minder contrast; onze crème strook (a) is fel.
3. **Verre oor.**
   - De steel is een lange zwarte lijn van 1 px over de bovenrand (rij 0, x24-38). Op 8× lijkt dat een beetje een antenne of hoedrand.
   - Hij ligt evenwijdig aan de steel van het nabije oor (rij 3). Dat leest als twee lijnen boven elkaar.
   - Hoger kan niet, want rij 0 is de bovenrand van het beeld.
4. **Buik.**
   - Waar de keel overgaat in de buik (rij 17 → 18) zit een stap van 2 px: een holle schouder onder de nek.
   - Op 8× is dat zichtbaar. Het is bewust, want anders blijft de rechte diagonaal van r6.
   - De buik is links 1-2 px voller dan in r6 (minder dan in r5).
5. **Leeg stuk.** Links van de kop, waar de oude verre krul zat, is nu een lege inham tussen de verre vleugel en de kop.
6. **Niet gekeurd.** Er is nog geen onafhankelijke keuring gedaan.

Er is niets gecommit en niets verwijderd.
