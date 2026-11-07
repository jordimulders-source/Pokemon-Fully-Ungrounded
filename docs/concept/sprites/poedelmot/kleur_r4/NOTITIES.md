# Poedelmot: kleur r4 (maker)

Jordi: "zo true to form als mogelijk" · "moet echt heel erg lijken op het model" · over r3: "nee blijf doorgaan, je bent op de goede weg".
r4 is gebouwd vanaf r3; r3 is niet aangeraakt. Overgenomen uit r3: de gebogen lijnen, de glimlachboog, de driekwart-kop, de schuine vleugelvoetlijn, de hangende pluimpootjes zonder donkere ring en de vleugels zonder letterkrullen.

## Bestanden
- `raster.txt` (bron), `palet.py` → `poedelmot.png` (geïndexeerd, index 0 transparant) + `normal.pal` (JASC, 16, veelvouden van 8; 9 en 13–15 ongebruikt).
- `vel.py` → `vel.png`: r4 | r3 | bron op 8×, r4 op 1×/2× licht en donker, close-ups 12× (ogen/gezicht, sprieten, pootjes, vleugels) r4 naast de bron.
- `controle.py` → `controle_uitvoer.txt` (leest `spriet_zone.txt`, `klauw_rand.txt`).
- `stappen/bouw4.sh`: r2 → tinten → kop (r3) → oog r4 → vleugels r4 → onderkant (r3) → sprieten r4 → opschonen → reparaties (r3) → warm maken → buitenlijn.

## Schaduwtint: de bron is leidend
De bronkleuren zijn per zone opnieuw gemeten (k-means op `samengesteld.png`):

| Zone | Gemeten kleuren |
|---|---|
| Borst/kraag | wit (254,247,243), crème (234,218,191), bruin (153,125,109) |
| Pootpluimen | wit, crème (232,216,192), grijsroze (176,154,143) |
| Voorvleugel | wit (253,245,240), crème (238,221,190), tan (212,184,161), (161,133,112) |
| Oog | zwart, met donker olijf (53,48,46)/(105,96,86) onderin |
| Achterlijf | (228,204,178), (192,159,138), (153,121,110) |

Gevolg:
- In het lijf staat geen lila meer. Schaduw is warm crème `7` (L218) en tan `6` (L188) onder wit `A` (L241).
- Alleen de pootpluimen houden de koele grijsroze `8` uit de bron.
- Vleugels: crème `7`, wit `A`, schubben `6`/`5`.

## Reparaties
1. **Sprieten**: terug naar de r2-basis.
   - Zwart vlak met één doorlopende lichte nerf `C`.
   - De baarden zijn fijne schuine streepjes van 1 px: `5`, onderaan `4`, om de 4 px, met af en toe een onderbreking. Daardoor geen raster.
   - Spaarzame donkerbruine kammetjes boven de nerf.
   - Het dambord uit r3 is weg.
2. **Nabij oog**: glanzend zwart amandeloog, iets schuin (rechtsboven hoog, linksonder laag), pupil zwart. Een schuine ovale glans van 2×2 linksboven, een zwakke donker-olijf reflectie (`B`, 4 px) onderin en een dunne tan ring eromheen. Het verre oog is zoals in r3 (smal, x16–19), ook met olijf in plaats van bruin.
3. **Vleugels**:
   - Overwegend licht crème met een witte buitenzone en lichte lobboogjes in de geschulpte rand.
   - Daarbinnen golvende tan schublijnen ("wolkjes") langs ringen rond de vleugelvoet. Naar de voet toe staan ze dichter en zijn ze donkerder (`5`), verder naar buiten lichter (`6`). De voet zelf is zacht tan.
   - De twee lagen blijven gescheiden door de geschulpte zoom; de achtervleugel heeft zijn eigen geschulpte onderrand.
4. **Vacht**: de plukjes op borst, kraag en kruin en de sikkels zijn nu warme schaduwtrekjes. Wit overheerst.

## Controle
- **Alpha-diff met silhouet: 0** (1782 = 1782).
- Open randen 0 (uitzonderingen: 4 klauwpixels en de rechtersprietpunt (52,18–19) in `4`).
- Selout: 9 reeksen zonder afwisseling.
- Losse pixels: 0. Tintclusters < 3 px: 0 (vlaktinten 5–9 en A; sprietzone en oogglans uitgezonderd).
- Donker-aandeel (1+2): **0,24** (eis ≤ 0,25).

## Hoofdvraag (zelf getoetst op 8× en 1× naast de bron)
- **Jordi's ontwerp?** Ja, dichter bij dan r3:
  - Warm wit donslijf, driekwart-kop met een groot glanzend zwart oog en een smal ver oog.
  - Zwarte geveerde sprieten met lichte nerf, crème vleugels met tan schubwolkjes en een witte rand, hangende pluimpootjes.
  - Op 1× herkenbaar als de poedelmot van de bron.
- **Wat ik nog anders zie dan de bron**:
  - **Sprietbaarden**: om de 4 px, ijler dan de dichte veertjes van de bron. Dichter maken gaf in r3 een dambord.
  - **Vleugelschubben**: de wolkjes zijn grover en minder rond dan Jordi's fijne krullen. De grote krul op de voorvleugel van de bron is hier een van de schublijnen, geen eigen vorm.
  - **Pluizige randen**: het silhouet is bevroren, dus de buitenrand blijft glad. Het pluizige komt alleen van de plukjes binnenin.
  - **Kop**: de koepel en de wangrand zijn minder duidelijk dan in de bron, omdat wit op wit weinig contrast heeft.
  - **Achterlijf**: in de bron grotendeels verstopt achter de pluimen. Hier is het nog iets meer zichtbaar.
- **Game Freak-stijl?** Omlijning, selout, ogen, warme schaduw van linksboven en de compositie kloppen. De schubbogen en de baarden zijn regelmatiger dan met de hand gezet.
- **Werkwijze**: de vleugelbogen, de pluimvormen, de sprietbaarden en de opschoning zijn met kleine scripts op mijn eigen ontwerp gezet. Middelpunten, stralen, pixellijsten en kleuren zijn met de hand op de bron gekozen en daarna nagewerkt.
